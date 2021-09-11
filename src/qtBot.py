from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QApplication
from PyQt5.uic import loadUiType

from web3 import Web3

import botUltilities

import sys
import os
from os import path
import sqlite3
import time

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


FORM_CLASS, _ = loadUiType(resource_path("qt-pkmon-bot.ui"))



class Main(QMainWindow, FORM_CLASS):

    monsters_list = []
    is_start = False
    my_account = ''
    my_private_key = ''

    def __init__(self, parent=None):
        super()
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.handle_buttons()

        self.w3 = botUltilities.connectBscNetwork()
        self.contract = botUltilities.load_contract(self.w3)
        self.load_config_database()
        self.timer = QTimer()
        self.timer.setInterval(1000)
        self.monster_round = 0

    def load_init(self):
        self.lb_status.setText('disconnect')
        self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)

    def handle_buttons(self):
        self.btn_show.clicked.connect(self.show_config_database)
        self.btn_save.clicked.connect(self.update_config_database)
        self.btn_connect.clicked.connect(self.connect_network)
        self.btn_remove_monster.clicked.connect(self.delete_monsters_database)
        self.btn_update.clicked.connect(self.update_monsters_database)
        self.tableWidget.cellClicked.connect(self.table_clicked)
        self.btn_start.clicked.connect(self.bot_start)

        self.actionExit.triggered.connect(self.action_exit)


    def load_monster_database(self):
        db = sqlite3.connect("pkmon.db")
        cursor = db.cursor()

        cmd_load_monster = ''' SELECT * FROM monsters_tbl '''

        result_monster = cursor.execute(cmd_load_monster)
        monters_in_db = result_monster.fetchall()
        db.close()

        self.monsters_list = []

        for monster in monters_in_db:
            self.monsters_list.append(monster)

        self.monster_view_reload()

    def monster_view_reload(self):
        self.tableWidget.setRowCount(0)

        for row_number, row_data in enumerate(self.monsters_list):
            self.tableWidget.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.tableWidget.setItem(row_number, column_number, QTableWidgetItem(str(data)))

    def show_config_database(self):
        db = sqlite3.connect("pkmon.db")
        cursor = db.cursor()
        cmd_load_config = ''' SELECT * FROM configs_tbl '''

        result_config = cursor.execute(cmd_load_config).fetchone()
        db.close()

        self.txt_acc.setText(result_config[1])
        self.txt_priv_key.setText(result_config[2])

    def load_config_database(self):
        db = sqlite3.connect("pkmon.db")
        cursor = db.cursor()
        cmd_load_config = ''' SELECT * FROM configs_tbl '''

        result_config = cursor.execute(cmd_load_config).fetchone()
        db.close()

        self.my_account = result_config[1]
        self.my_private_key = result_config[2]

    def update_config_database(self):
        acc = self.txt_acc.toPlainText()
        key = self.txt_priv_key.toPlainText()

        db = sqlite3.connect("pkmon.db")
        cursor = db.cursor()

        cmd_update_config = '''UPDATE configs_tbl SET account='{0}' WHERE id={1}'''.format(acc, 1)
        cursor.execute(cmd_update_config)
        cmd_update_config = ''' UPDATE configs_tbl SET private_key='{0}'  WHERE id={1}'''.format(key, 1)
        cursor.execute(cmd_update_config)

        db.commit()
        db.close()

        self.my_account = acc
        self.my_private_key = key

    def delete_monsters_database(self):

        db = sqlite3.connect("pkmon.db")
        cursor = db.cursor()

        row = self.tableWidget.currentRow()

        monster_row = self.monsters_list[row]

        cmd_delete = 'DELETE FROM monsters_tbl WHERE id={0}'.format(monster_row[0])
        cursor.execute(cmd_delete)
        db.commit()

        '''reload DB'''
        self.load_monster_database()

    def update_monsters_database(self):
        db = sqlite3.connect("pkmon.db")
        cursor = db.cursor()

        monster_id = self.txt_monster_id_update.toPlainText()
        monster_round = self.txt_monster_rat_update.toPlainText()

        '''check monsters is in list, if yes update, if not add new'''
        monster_index = self.find_monster_in_list(monster_id)

        if monster_index == 0:
            cmd_update_or_insert = 'INSERT INTO "main"."monsters_tbl"("Monster","MaxRound") VALUES ({0},{1});'.format(monster_id, monster_round)
        else:
            cmd_update_or_insert = 'UPDATE monsters_tbl SET Monster={1}, MaxRound={2} WHERE id={0}'.format(monster_index, monster_id, monster_round)

        cursor.execute(cmd_update_or_insert)
        db.commit()
        db.close()
        '''reload DB'''
        self.load_monster_database()

    def table_clicked(self):

        row = self.tableWidget.currentRow()
        monster_row = self.monsters_list[row]

        self.txt_monster_id_update.setPlainText(str(monster_row[1]))
        self.txt_monster_rat_update.setPlainText(str(monster_row[3]))

    def action_exit(self):
        self.close()

    def bot_start(self):

        if not self.is_start:
            self.btn_start.setText('Stop')
            self.is_start = True

        else:
            self.btn_start.setText('Start')
            self.is_start = False
            self.timer.stop()

        ''' bot start '''
        if self.is_start:
            self.timer = QTimer()
            self.timer.setInterval(1000)
            self.timer.timeout.connect(self.main_loop_monster)
            self.timer.start()

    def main_loop_monster(self):
        monster_round = self.monster_round

        if self.is_start:
            self.txt_log.append("--- round {0} ---".format(monster_round))
            for monster in self.monsters_list:

                battle_round = 1
                while battle_round < monster[3] + 1:
                    is_bot_ready = botUltilities.is_ready_to_battle(monster[1], self.contract, battle_round)

                    if is_bot_ready:
                        tx = botUltilities.monster_battle(monster[1], self.w3, self.my_account, self.my_private_key)
                        self.txt_log.append(
                            "Monster {0} --- battle {1} --- Tx {2}".format(monster[1], battle_round, tx))

                    else:
                        total_battle = botUltilities.get_total_battle_times(monster[1], self.contract)
                        last_battle_time = botUltilities.get_last_battle_time(monster[1], total_battle,
                                                                              self.contract)
                        next_battle = last_battle_time + botUltilities.get_next_battle_time(3) + 30

                        self.txt_log.append("Monster {0} next battle at {1} secs".format(monster[1],
                                                                                next_battle - botUltilities.get_current_time()))
                        break

                    battle_round += 1
                    self.txt_log.append(" ")
                    time.sleep(5)
            ''' end For '''

        if self.is_start:
            self.timer = QTimer()
            self.timer.setInterval(300000)
            self.timer.timeout.connect(self.main_loop_monster)
            self.timer.start()

        self.monster_round += 1
        '''sleep 5 min and check again '''
        self.txt_log.append("next check in 5 mins")
        self.txt_log.append(" ")
        self.txt_log.append(" ")

        ''' end While True '''

    def connect_network(self):
        self.w3 = botUltilities.connectBscNetwork()

        if self.w3.isConnected():
            self.lb_status.setText('connected, Free version')

    def find_monster_in_list(self, monster_id):
        index = 0

        for monster in self.monsters_list:
            if str(monster_id) == str(monster[1]):
                index = monster[0]
                break
            else:
                continue

        return index

    def check_license(self):
        return False

def main():
    app = QApplication(sys.argv)
    window = Main()
    window.load_init()
    window.load_monster_database()

    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
