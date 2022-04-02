import platform

import dearpygui.dearpygui as dpg

import init_values
import item_callbacks
import utils


def init_values_sys():
    with dpg.value_registry():
        dpg.add_bool_value(tag='is_connected', default_value=False)
        dpg.add_bool_value(tag='is_connecting',default_value=False)
        dpg.add_string_value(tag='session_manager_connecting_btn_tag',default_value='')
        dpg.add_int_value(tag='editing_scene_index',default_value=0)
        dpg.add_string_value(tag='selected_topic',default_value='')



def init_custom_themes():
    with dpg.theme(tag='btn_theme_yellow'):
        with dpg.theme_component(dpg.mvButton):
            dpg.add_theme_color(dpg.mvThemeCol_Button, utils.Hex_to_RGB('#FFFF66'))  # normal
            dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, utils.Hex_to_RGB('#FFFF00'))  # 点住
            dpg.add_theme_color(dpg.mvThemeCol_Text, utils.Hex_to_RGB('#000000'))  # 字颜色
            dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, utils.Hex_to_RGB('#FFFF00'))  # hover
            dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 5)
            dpg.add_theme_style(dpg.mvStyleVar_FramePadding, 3, 3)

    with dpg.theme(tag='btn_theme_red'):
        with dpg.theme_component(dpg.mvButton):
            dpg.add_theme_color(dpg.mvThemeCol_Button, utils.Hex_to_RGB('#FF6666'))  # normal
            dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, utils.Hex_to_RGB('#FF0033'))  # 点住
            dpg.add_theme_color(dpg.mvThemeCol_Text, utils.Hex_to_RGB('#000000'))  # 字颜色
            dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, utils.Hex_to_RGB('#FF0033'))  # hover
            dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 5)
            dpg.add_theme_style(dpg.mvStyleVar_FramePadding, 3, 3)

    with dpg.theme(tag='left_tree_bg_theme'):
        with dpg.theme_component(dpg.mvChildWindow):
            dpg.add_theme_color(dpg.mvThemeCol_ChildBg, utils.Hex_to_RGB('#333333'))
    with dpg.theme(tag='btn_theme_red_blink'):
        with dpg.theme_component(dpg.mvButton):
            dpg.add_theme_color(dpg.mvThemeCol_Button, utils.Hex_to_RGB('#FF6666'))  # normal

    with dpg.theme(tag='btn_theme_message_blue'):
        with dpg.theme_component(dpg.mvButton):
            dpg.add_theme_color(dpg.mvThemeCol_Button, utils.Hex_to_RGB('#479BF7'))  # normal
            dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, utils.Hex_to_RGB('#316BAB'))  # 点住
            dpg.add_theme_color(dpg.mvThemeCol_Text, utils.Hex_to_RGB('#FFFFFF'))  # 字颜色
            dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, utils.Hex_to_RGB('#3D86D6'))  # hover
            dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 5)
            dpg.add_theme_style(dpg.mvStyleVar_FramePadding, 3, 3)


def init_font_resource():
    with dpg.font_registry():
        english_font_bold = dpg.add_font(tag="english_font_bold", file="fonts/SourceCodePro-Bold.otf",
                                         size=16)  # 英文字体粗体 16px
        english_font_normal = dpg.add_font(tag='english_font_normal', file="fonts/SourceCodePro-Regular.otf",
                                           size=16)  # 英文字体常规体 16px
        sf_mono_for_apple_user = dpg.add_font(file='fonts/SFMono-Regular.otf', tag='sf_mono_for_apple_user', size=16)
        with dpg.font(tag='chinese_font', file="fonts/SourceHanSansSC-Normal.otf",
                      size=16) as chinese_font:  # 中文字体 默认界面字体
            dpg.add_font_range_hint(dpg.mvFontRangeHint_Default)
            dpg.add_font_range_hint(dpg.mvFontRangeHint_Chinese_Simplified_Common)
            dpg.add_font_range_hint(dpg.mvFontRangeHint_Chinese_Full)


def init_main_window():
    with dpg.window(tag='bg_window', no_resize=True):
        with dpg.menu_bar():
            with dpg.menu(label="Connection"):
                dpg.add_menu_item(tag='btn_quick_connect', label="Quick connect", callback=item_callbacks.quick_connect)
                dpg.add_menu_item(tag='btn_disconnect', label="Disconnect",
                                  callback=item_callbacks.btn_disconnect_callback)
                dpg.add_menu_item(tag='session_manager', label="Session Manager",
                                  callback=item_callbacks.btn_session_manager)
            with dpg.menu(label="Subscribtion"):
                dpg.add_menu_item(tag='btn_subscribtion', label="New subscribtion", callback=item_callbacks.print_me)
                dpg.add_menu_item(tag='btn_subscribtion_manage', label="Subscribtion management",
                                  callback=item_callbacks.print_me)

            with dpg.menu(label='Mode'):
                dpg.add_radio_button(items=['Normal Mode', 'Sniff Mode'], callback=item_callbacks.print_me,
                                     default_value='Sniff Mode')
            with dpg.menu(label="Settings"):
                dpg.add_menu_item(label="Basic setting", callback=item_callbacks.print_me)
            with dpg.menu(label="Help"):
                dpg.add_menu_item(label="About", callback=item_callbacks.btn_about_callback)
                if init_values.DEBUG:
                    dpg.add_menu_item(label="Font Manager", callback=item_callbacks.btn_font_manager_callback)
                    dpg.add_menu_item(label="Show demo", callback=item_callbacks.btn_demo_callback)
                    dpg.add_menu_item(label="Show docu", callback=item_callbacks.btn_document_callback)
                    dpg.add_menu_item(label="Show debug", callback=item_callbacks.btn_debug_callback)
        with dpg.group(horizontal=True):
            with dpg.child_window(width=1050, tag='left_sub_window', horizontal_scrollbar=True,border=True):
                dpg.bind_item_theme('left_sub_window', 'left_tree_bg_theme')
            with dpg.child_window(width=1440 - 1050 - 10 - 14,height=900-24-14, border=False):
                # dpg.add_button(label='btn2', width=100, height=100, callback=item_callbacks.tree_test_callback)
                with dpg.tab_bar():
                    with dpg.tab(label='Message'):
                        with dpg.child_window(height=900-24-14-55,border=False,tag='message_history_area'):
                            pass
                    with dpg.tab(label='detail'):
                        with dpg.child_window(height=900 - 24 - 14 - 55, border=False):
                            dpg.add_text('111')
                    with dpg.tab(label='stat'):
                        with dpg.child_window(height=900 - 24 - 14 - 55, border=False):
                            dpg.add_text('111')
                dpg.add_text('Connect Status: Disconnected', tag='mqtt_connect_status',color=(255,0,0))

    dpg.set_primary_window('bg_window', True)


def init_about_window():
    with dpg.window(label='About',tag='about_window', pos=(100, 100),
                    show=False, width=250, height=350,
                    no_resize=True, no_collapse=True,
                    on_close=item_callbacks.about_window_close):
        width,height,channels,data = dpg.load_image(file='img/logo_bm_new.png')
        with dpg.texture_registry(show=False):
            dpg.add_static_texture(width,height,data,tag='logo')
        dpg.add_image('logo',width=200,height=200)
        about_title = f'Better MQTT {init_values.VERSION}'
        with dpg.group(horizontal=True,horizontal_spacing=1,tag='about_text'):
            r = 0
            for ch in about_title:
                title = dpg.add_text(ch)
                init_values.ABOUT_TEXTS.append(title)
                dpg.bind_item_font(title, 'english_font_bold')
        for author in init_values.AUTHORS:
            dpg.add_text(f'Author:{author}', bullet=True)

def set_font():
    plantform_name = platform.system()
    if plantform_name == 'Darwin':
        dpg.bind_font('sf_mono_for_apple_user')
    else:
        dpg.bind_font('english_font_bold')



def init_disconnect_modal():
    # disconnect modal
    with dpg.window(label="Disconnect", modal=True, height=100, no_resize=True, show=False,
                    tag='conform_disconnect_modal'):
        dpg.add_text("Are you sure to disconnect?")
        with dpg.group(horizontal=True, horizontal_spacing=40):
            dpg.add_button(label="Yes", width=75, callback=item_callbacks.btn_disconnect_yes)
            dpg.add_button(label="No", width=75,
                           callback=lambda: dpg.configure_item("conform_disconnect_modal", show=False))


def init_quick_connect_modal():
    # quick connect window
    with dpg.window(label='Quick Connect', width=360, height=200, no_resize=True, show=False, modal=True,
                    tag='quick_connect_window'):
        dpg.add_input_text(label='HOST', tag='quickconnect_host_input')
        dpg.add_input_int(label='PORT', tag='quickconnect_port_input', default_value=1883, step=0)
        dpg.add_input_text(label='Username', tag='quickconnect_username_input')
        dpg.add_input_text(label='Password', password=True, tag='quickconnect_password_input')
        with dpg.collapsing_header(label='Advance options'):
            dpg.add_input_text(label='TLS', default_value=60)
        with dpg.group(horizontal=True, tag='qucik_connect_button_group'):
            dpg.add_button(label='Connect', callback=item_callbacks.do_connect, tag='qucik_connect_btn_connect')
            dpg.add_loading_indicator(parent='qucik_connect_button_group', tag='quick_connect_loading_indicator',
                                      radius=1.5, style=1, show=False)


def init_session_manager_window():
    # session manager
    with dpg.window(label='Session Manager', height=520, no_resize=True, show=False, tag='session_manager_window',
                    no_collapse=True):
        with dpg.table(header_row=True, row_background=True,
                       borders_innerH=True, borders_outerH=True, borders_innerV=True,
                       borders_outerV=True, delay_search=True, width=600, height=450, scrollY=True, clipper=True,
                       freeze_rows=1, tag='session_table') as table_id:
            dpg.add_table_column(label="ALIAS")
            dpg.add_table_column(label="HOST")
            dpg.add_table_column(label="PORT")
            dpg.add_table_column(label="")
            # init session table
            for index, data in enumerate(init_values.SESSIONS):
                with dpg.table_row():
                    with dpg.table_cell():
                        dpg.add_text(data['alias'])
                    with dpg.table_cell():
                        dpg.add_text(data['host'])
                    with dpg.table_cell():
                        dpg.add_text(data['port'])
                    with dpg.table_cell():
                        with dpg.group(horizontal=True):
                            dpg.add_button(label="CONNECT",
                                           callback=item_callbacks.btn_session_manager_connect_callback,
                                           user_data={'data': data, 'tag': 'session_connect_btn_tag_' + str(index)},
                                           tag='session_connect_btn_tag_' + str(index))
                            dpg.bind_item_theme(dpg.last_item(), "btn_theme_red")
                            dpg.add_button(label="EDIT", callback=item_callbacks.btn_session_manager_edit_callback,
                                           user_data={'data': data, 'index': index})
                            dpg.bind_item_theme(dpg.last_item(), "btn_theme_yellow")
        with dpg.group(horizontal=True):
            dpg.add_button(label='Add')
            dpg.add_button(label='Remove')
            dpg.add_loading_indicator(tag='session_manager_loading_indicator',
                                      radius=1.5, style=1, show=False)

def init_session_add_edit_window():
    # session add/edit
    with dpg.window(label='Add/Edit Session', width=360, no_resize=True, show=False, modal=True,
                    tag='edit_session_window'):
        dpg.add_input_text(label='ALIAS', tag='edit_session_alias_input')
        dpg.add_input_text(label='HOST', tag='edit_session_host_input')
        dpg.add_input_int(label='PORT', tag='edit_session_port_input', default_value=1883, step=0)
        dpg.add_input_text(label='Username', tag='edit_session_username_input')
        dpg.add_input_text(label='Password', password=True, tag='edit_session_password_input')
        with dpg.collapsing_header(label='Advance options'):
            dpg.add_input_text(label='TLS', default_value=60)
        with dpg.group(horizontal=True):
            dpg.add_button(label='OK', callback=item_callbacks.edit_session_ok_btn_callback)
            dpg.add_button(label='Cancel', callback=item_callbacks.edit_session_cancel_btn_callback)
