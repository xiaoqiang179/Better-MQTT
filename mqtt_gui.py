import dearpygui.dearpygui as dpg

import init_funcs
import init_values
import item_callbacks

dpg.create_context()
# init custom theme
init_funcs.init_custom_themes()
# init font resource
init_funcs.init_font_resource()
# set font
init_funcs.set_font()
# init main window
init_funcs.init_main_window()
init_funcs.init_disconnect_modal()
init_funcs.init_quick_connect_modal()
init_funcs.init_session_manager_window()
init_funcs.init_session_add_edit_window()
init_funcs.init_about_window()
init_funcs.init_values_sys()
dpg.set_viewport_resize_callback(item_callbacks.viewport_resize_callback)
dpg.set_exit_callback(item_callbacks.exit_callback)


dpg.create_viewport(title='Better MQTT', width=1440, height=900, resizable=False,
                    large_icon='img/logo_bm_new.png')

dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()
