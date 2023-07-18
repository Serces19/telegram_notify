import nuke
import re
import os

write_node = nuke.thisNode()
render_path = nuke.filename(write_node)
nueva_extension = "proxy.mp4"
render_path_proxy = re.sub(r"\.\w+$", "." + nueva_extension, render_path)

def render_proxy():
    write_node = nuke.thisNode()
    if write_node['telegram_notify'].value() is False:
        return

    if not os.path.exists(render_path):
        return

    with nuke.nodes.Group() as group:
        
        # Crear un nodo Read para cargar el archivo de entrada
        read_node = nuke.createNode("Read")
        read_node["file"].fromUserText(render_path)
        read_node['frame_mode'].setValue('start at')
        first_frame = nuke.root().firstFrame()
        first_frame = str(first_frame)
        last_frame = nuke.root().lastFrame()
        last_frame = str(last_frame)
        read_node['frame'].setValue(first_frame)


        # Crear un nodo Reformat para reducir la escala a 1/4
        reformat_node = nuke.createNode("Reformat")
        reformat_node["type"].setValue("scale")
        reformat_node["scale"].setValue(0.25)

        # Conectar el nodo Read al nodo Reformat
        reformat_node.setInput(0, read_node)

        # Crear un nodo Write para escribir el archivo de salida
        write_node = nuke.createNode("Write")
        write_node["file"].fromUserText(render_path_proxy)
        write_node["colorspace"].setValue("sRGB")
        write_node["file_type"].setValue("mov")  # Establecer el tipo de archivo a MOV
        write_node["mov64_codec"].setValue("h264")  # Establecer el códec a H.264
        write_node["mov64_quality"].setValue("Least")  # Establecer la calidad a baja


        # Conectar el nodo Reformat al nodo Write
        write_node.setInput(0, reformat_node)
        nuke.execute(write_node)

    nuke.delete(group)