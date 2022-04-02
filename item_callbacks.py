import json
import math
import random
import sys
import threading
import time
import uuid

import dearpygui.dearpygui as dpg
import dearpygui.demo as demo
import pyperclip

import init_values
import mqtt_client
import mqtt_client as client

sys.setrecursionlimit(3000)
about_window_flag = True


def about_window_close():
    global about_window_flag
    about_window_flag = True


def hsv2rgb(h, s, v):
    h = float(h)
    s = float(s)
    v = float(v)
    h60 = h / 60.0
    h60f = math.floor(h60)
    hi = int(h60f) % 6
    f = h60 - h60f
    p = v * (1 - s)
    q = v * (1 - f * s)
    t = v * (1 - (1 - f) * s)
    r, g, b = 0, 0, 0
    if hi == 0: r, g, b = v, t, p
    elif hi == 1: r, g, b = q, v, p
    elif hi == 2: r, g, b = p, v, t
    elif hi == 3: r, g, b = p, q, v
    elif hi == 4: r, g, b = t, p, v
    elif hi == 5: r, g, b = v, p, q
    r, g, b = int(r * 255), int(g * 255), int(b * 255)
    return r, g, b


def change_color(all_char):
    global about_window_flag
    h = 0
    while True:
        if about_window_flag == True:
            break
        for item in all_char:
            dpg.configure_item(item, color=hsv2rgb(h, 1, 1))
            h += 10
            h %= 361
            time.sleep(0.1)


# 菜单栏about的回调
def btn_about_callback(sender, app_data, user_data):
    dpg.configure_item('about_window', show=True)
    global about_window_flag
    about_window_flag = False
    threading.Thread(target=change_color, args=([init_values.ABOUT_TEXTS])).start()


# 测试方法
def print_me(sender, app_data, user_data):
    print(f'clicked {sender} app_data {app_data} user_data {user_data}')


# 菜单栏字体管理器的回调
def btn_font_manager_callback(sender, app_data, user_data):
    dpg.show_font_manager()


# 菜单栏断开连接的回调
def btn_disconnect_callback(sender, app_data, user_data):
    if dpg.get_value('is_connected') == False:
        return
    dpg.configure_item("conform_disconnect_modal", show=True)


# 菜单栏session manager的回调
def btn_session_manager(sender, app_data, user_data):
    dpg.configure_item('session_manager_window', show=True)
    refresh_session_table()


# 清空sniff mode的树
def clean_left_tree():
    dpg.delete_item('left_sub_window', children_only=True)


# 断开连接yes按钮的回调
def btn_disconnect_yes(sender, app_data, user_data):
    dpg.configure_item("conform_disconnect_modal", show=False)
    dpg.set_value('is_connected', False)
    client.disconnect()


# 关闭窗口的回调
def exit_callback(sender, app_data, user_data):
    client.disconnect()


# 菜单栏展示demo的回调
def btn_demo_callback(sender, app_data, user_data):
    threading.Thread(target=demo.show_demo).start()


# 菜单栏展示文档的回调
def btn_document_callback(sender, app_data, user_data):
    dpg.show_documentation()


# 菜单栏展示debug的回调
def btn_debug_callback(sender, app_data, user_data):
    dpg.show_debug()


# view_port resize时的回调
def viewport_resize_callback(sender, app_data, user_data):
    pass
    # print(sender, app_data, user_data)


# 测试树性能的 添加树节点 800层
def add_tree_data(parent_tag, level):
    if level > 800:
        dpg.add_tree_node(label='leaf', parent=parent_tag, leaf=True)
        dpg.add_tree_node(label='leaf11', parent=parent_tag)
        return
    id = dpg.add_tree_node(label=str(random.randint(1, 10)) + ' ' + str(uuid.uuid1()), parent=parent_tag,
                           default_open=True)
    add_tree_data(id, level + 1)


#
def tree_test_callback(sender):
    print(sender)
    add_tree_data('left_sub_window', 1)


# 菜单栏quick connect的回调
def quick_connect(sender, app_data, user_data):
    dpg.configure_item("quick_connect_window", show=True)


# 清空quick connect窗口的回调
def clean_quick_connect_form():
    dpg.set_value('quickconnect_username_input', '')
    dpg.set_value('quickconnect_password_input', '')
    dpg.set_value('quickconnect_host_input', '')
    dpg.set_value('quickconnect_port_input', 1883)


# 连接方法 开启一个线程 连接
def connect(host, port, username, password):
    client.HOST_NAME = host
    client.PORT = port
    client.USER_NAME = username
    client.PASSWORD = password
    client.connect()
    client.subscribe('#')
    th_mqtt = threading.Thread(target=client.start_loop)
    th_mqtt.start()


# quick connect ok button
def do_connect(sender, app_data, user_data):
    if user_data is not None and user_data.get('cancel_quick_connect') is not None:  # 代表点了连接之后
        client.disconnect()
        dpg.configure_item('qucik_connect_btn_connect', label='Connect')
        dpg.configure_item('qucik_connect_btn_connect', user_data={})
        dpg.configure_item('quick_connect_loading_indicator', show=False)  # quick connect的转圈
        return
    username = dpg.get_value('quickconnect_username_input')
    password = dpg.get_value('quickconnect_password_input')
    host = dpg.get_value('quickconnect_host_input')
    port = dpg.get_value('quickconnect_port_input')
    connect(host, port, username, password)
    dpg.configure_item('qucik_connect_btn_connect', label='Cancel')
    dpg.configure_item('qucik_connect_btn_connect', user_data={'cancel_quick_connect': 1})
    dpg.configure_item('quick_connect_loading_indicator', show=True)


# 刷新session的表格
def refresh_session_table():
    dpg.delete_item('session_table', children_only=True)
    dpg.add_table_column(label="ALIAS", parent='session_table')
    dpg.add_table_column(label="HOST", parent='session_table')
    dpg.add_table_column(label="PORT", parent='session_table')
    dpg.add_table_column(label="", parent='session_table')
    # init session table
    for index, data in enumerate(init_values.SESSIONS):
        with dpg.table_row(parent='session_table'):
            with dpg.table_cell():
                dpg.add_text(data['alias'])
            with dpg.table_cell():
                dpg.add_text(data['host'])
            with dpg.table_cell():
                dpg.add_text(data['port'])
            with dpg.table_cell():
                with dpg.group(horizontal=True):
                    dpg.add_button(label="CONNECT", callback=btn_session_manager_connect_callback,
                                   user_data={'data': data, 'tag': 'session_connect_btn_tag_' + str(index)},
                                   tag='session_connect_btn_tag_' + str(index))
                    dpg.bind_item_theme(dpg.last_item(), "btn_theme_red")
                    dpg.add_button(label="EDIT", callback=btn_session_manager_edit_callback,
                                   user_data={'data': data, 'index': index})
                    dpg.bind_item_theme(dpg.last_item(), "btn_theme_yellow")


# 点击session中任意一行连接按钮的回调
def btn_session_manager_connect_callback(sender, app_data, user_data):
    print(user_data)
    if user_data.get('is_connecting') is not None:  # 点了Cancel
        dpg.configure_item('session_manager_loading_indicator', show=False)
        dpg.configure_item(user_data['tag'], label='CONNECT')
        del user_data['is_connecting']
        dpg.set_value('is_connecting', False)
        client.disconnect()
        return
    if dpg.get_value('is_connecting') or dpg.get_value('is_connected'):
        return
    dpg.set_value('is_connecting', True)
    dpg.configure_item('session_manager_loading_indicator', show=True)
    dpg.configure_item(user_data['tag'], label='CANCEL')
    dpg.set_value('session_manager_connecting_btn_tag', user_data['tag'])
    connect_info = user_data['data']
    user_data['is_connecting'] = 1
    connect(connect_info['host'], connect_info['port'], connect_info['username'], connect_info['password'])


# 设置session manager添加、编辑窗口的form
def set_session_add_edit_data(alias, host, port, username, password):
    dpg.set_value('edit_session_alias_input', alias)
    dpg.set_value('edit_session_host_input', host)
    dpg.set_value('edit_session_port_input', port)
    dpg.set_value('edit_session_username_input', username)
    dpg.set_value('edit_session_password_input', password)


# 获取session manager添加、编辑窗口的form的数据
def get_session_add_edit_data():
    alias = dpg.get_value('edit_session_alias_input')
    host = dpg.get_value('edit_session_host_input')
    port = dpg.get_value('edit_session_port_input')
    username = dpg.get_value('edit_session_username_input')
    password = dpg.get_value('edit_session_password_input')
    ret_val = {
        'alias': alias,
        'host': host,
        'port': port,
        'username': username,
        'password': password
    }
    return ret_val


def btn_session_manager_edit_callback(sender, app_data, user_data):
    if user_data is not None:
        set_session_add_edit_data(user_data['data']['alias'], user_data['data']['host'], user_data['data']['port'],
                                  user_data['data']['username'], user_data['data']['password'])
        dpg.set_value('editing_scene_index', user_data['index'])
        dpg.configure_item('edit_session_window', show=True)
        print(user_data)


def edit_session_cancel_btn_callback(sender, app_data, user_data):
    dpg.configure_item('edit_session_window', show=False)


#
def edit_session_ok_btn_callback(sender, app_data, user_data):
    dpg.configure_item('edit_session_window', show=False)
    index = dpg.get_value('editing_scene_index')
    init_values.SESSIONS[index] = get_session_add_edit_data()
    refresh_session_table()


# 拷贝user_data到剪贴板
def copy_data_to_clipboard(sender, app_data, user_data):
    pyperclip.copy(user_data)


def change_right_topic(sender, app_data, user_data):
    #add data to message_history_area
    dpg.delete_item('message_history_area',children_only=True)
    dpg.set_value('selected_topic',user_data['topic'])
    for data in mqtt_client.TOPIC_CACHE[user_data['topic']]:
        formatted_data = json.dumps(json.loads(data),indent=2)
        add_btn = dpg.add_button(label=formatted_data,parent='message_history_area')
        dpg.bind_item_theme(add_btn,'btn_theme_message_blue')
        with dpg.mutex():
            bottom = dpg.get_y_scroll_max('message_history_area')
            dpg.set_y_scroll('message_history_area', bottom+1)
