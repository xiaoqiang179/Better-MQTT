import datetime
import json
import threading
import time
import uuid

import dearpygui.dearpygui as dpg
import paho.mqtt.client as mqtt

import item_callbacks

USER_NAME = ''
PASSWORD = ''
HOST_NAME = ''
PORT = 1883
TREE_DATA = []
TOPIC_CACHE = {}
'''
{
    label:'树显示的标签',
    id:'gui的UUID',
    child:'是一个数组 代表孩子节点 是递归的结构',
    is_leaf:'是否是叶子节点',
    data:'叶子节点的数据',
}
'''


def on_connect(client, userdata, flags, rc):
    '''
        0-连接成功
        1-协议版本错误
        2-无效的客户端标识
        3-服务器无法使用
        4-错误的用户名或密码
        5-未经授权
    '''
    if rc == 0:
        dpg.set_value('is_connected',True) #代表已经连接
        dpg.set_value('is_connecting',False) #代表正在连接结束
        dpg.configure_item('quick_connect_loading_indicator',show=False) #quick connect的转圈
        dpg.configure_item('session_manager_loading_indicator', show=False)
        dpg.configure_item('qucik_connect_btn_connect', label='Connect')
        item_callbacks.clean_quick_connect_form()
        dpg.configure_item("quick_connect_window", show=False)
        dpg.set_value('mqtt_connect_status', 'Connect Status: Connected')
        dpg.configure_item('mqtt_connect_status',color=(0,255,0))
        if dpg.get_value('session_manager_connecting_btn_tag') != '':
            dpg.configure_item(dpg.get_value('session_manager_connecting_btn_tag'),label='CONNECT')
            user_data = dpg.get_item_user_data(dpg.get_value('session_manager_connecting_btn_tag'))
            if user_data.get('is_connecting') is not None:
                del user_data['is_connecting']
        dpg.configure_item('session_manager_window',show=False)

    print(client, 'connected with code:', mqtt.error_string(rc))


def on_disconnect(client, userdata, rc):
    global TREE_DATA
    TREE_DATA = []
    item_callbacks.clean_left_tree()
    dpg.set_value('mqtt_connect_status', 'Connect Status: Disconnected')
    dpg.configure_item('mqtt_connect_status', color=(255, 0, 0))
    print(client, 'disconnect with code:', mqtt.error_string(rc))


#             路径数组    层级    叶节点数据   当前层TREEDATA数据 是一个数组
def build_tree(path_arr:list, level:int, data:str, current_tree_level:list,parent_id,path):
    if level >= len(path_arr):
        cutted_data = data[0:100]+'....'
        if len(current_tree_level) > 0:
            dpg.configure_item(current_tree_level[0]['id'],label=cutted_data)
            dpg.configure_item(current_tree_level[0]['id'],user_data={'topic':path,'data':data})
            dpg.bind_item_theme(current_tree_level[0]['id'],'btn_theme_red_blink')
            time.sleep(0.2)
            dpg.bind_item_theme(current_tree_level[0]['id'],0)
            formatted_json = json.dumps(json.loads(data),indent=2)
            dpg.set_value(current_tree_level[0]['tooltip_id'],formatted_json)
            dpg.configure_item(current_tree_level[0]['copy_raw_data'],user_data=data)
            dpg.configure_item(current_tree_level[0]['copy_json_data'],user_data=formatted_json)
        else:
            new_node = dpg.add_button(label=cutted_data, parent=parent_id,callback=item_callbacks.change_right_topic,user_data={'topic':path,'data':data})
            with dpg.tooltip(new_node):
                add_tooltip_text = dpg.add_text(json.dumps(json.loads(data),indent=2))
            with dpg.popup(new_node):
                dpg.add_selectable(label='Publish')
                dpg.add_selectable(label='Add to subscribtion')
                copy_raw_data = dpg.add_selectable(label='Copy data(Raw)',callback=item_callbacks.copy_data_to_clipboard,user_data=data)
                copy_json_data = dpg.add_selectable(label='Copy data(Formatted JSON)',callback=item_callbacks.copy_data_to_clipboard,user_data=json.dumps(json.loads(data),indent=2))
            add_node = {
                'label': cutted_data,
                'id': new_node,
                'child': [],
                'tooltip_id':add_tooltip_text,
                'is_leaf': False,
                'data': data,
                'copy_raw_data':copy_raw_data,
                'copy_json_data':copy_json_data
            }
            current_tree_level.append(add_node)
        return
    current_path = path_arr[level]
    found = False
    for node in current_tree_level:
        if node['label'] == current_path:
            found = True
            build_tree(path_arr,level+1,data,node['child'],node['id'],path)
    if found == False: #说明当前路径是没有的 需要新建节点
        new_node = dpg.add_tree_node(label=current_path,parent=parent_id,default_open=True)
        add_node = {
            'label': current_path,
            'id': new_node,
            'child': [],
            'is_leaf': False,
            'data': '',
        }
        current_tree_level.append(add_node)
        build_tree(path_arr,level+1,data,add_node['child'],new_node,path)


def on_message(client, userdata, message):
    str_msg = message.payload.decode()
    if TOPIC_CACHE.get(message.topic) is None:
        TOPIC_CACHE[message.topic] = []
    TOPIC_CACHE[message.topic].append(str_msg)
    if dpg.get_value('selected_topic') == message.topic:
        add_btn = dpg.add_button(label=json.dumps(json.loads(str_msg),indent=2),parent='message_history_area')
        dpg.bind_item_theme(add_btn, 'btn_theme_message_blue')
        with dpg.mutex():
            bottom = dpg.get_y_scroll_max('message_history_area')
            dpg.set_y_scroll('message_history_area', bottom)
    topic_splited = message.topic.split('/')
    th = threading.Thread(target=build_tree,args=(topic_splited,0,str_msg,TREE_DATA,'left_sub_window',message.topic))
    th.start()



def on_publish(client, userdata, mid):
    print('published:', mid)


def on_subscribe(client, userdata, mid, granted_qos):
    print('subscribed topic:', mid)


def on_unsubscribe(client, userdata, mid):
    pass


client = mqtt.Client(str(uuid.uuid1()))
client.on_connect = on_connect
client.on_disconnect = on_disconnect
client.on_message = on_message
client.on_publish = on_publish
client.on_subscribe = on_subscribe
client.on_unsubscribe = on_unsubscribe


def connect():
    client.username_pw_set(username=USER_NAME,
                           password=PASSWORD)
    client.connect(HOST_NAME, PORT)


def subscribe(topic):
    client.subscribe(topic)


def publish(topic, payload):
    client.publish(topic, payload)


def start_loop():
    client.loop_forever()


def disconnect():
    client.disconnect()


if __name__ == '__main__':
    build_tree(['a','b','c','d'],0,'hahaha',TREE_DATA,'')
    build_tree(['a','b','c','e'],0,'hahaha',TREE_DATA,'')
    build_tree(['a','b','c','f'],0,'hahaha',TREE_DATA,'')
    build_tree(['a','b','c','d','ee'],0,'hahaha',TREE_DATA,'')
    print(json.dumps(TREE_DATA,indent=2))