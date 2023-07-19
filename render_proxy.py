import nuke

class render_proxy():

    def __init__(self, render_path, render_path_proxy, colorspace):
        self.render_path = render_path
        self.render_path_proxy = render_path_proxy
        self.colorspace = str(colorspace)
        print(render_path, render_path_proxy)
    
    def render_mp4(self):
        nuke.root()['lock_range'].setValue(True)

        with nuke.nodes.Group() as group:
            # Read
            read_node = nuke.createNode("Read")
            read_node["file"].fromUserText(self.render_path)
            first_frame = nuke.root().firstFrame()
            first_frame = str(first_frame)
            last_frame = nuke.root().lastFrame()
            last_frame = str(last_frame)
            read_node['frame_mode'].setValue('start at')
            read_node['frame'].setValue(first_frame)
            print(first_frame, last_frame)

            file_extension = self.render_path.split('.')[-1].lower()

            if file_extension not in ['mov', 'mp4', 'mxf']:
                read_node["first"].setValue(int(first_frame))
                read_node["last"].setValue(int(last_frame))


            # Reformat
            reformat_node = nuke.createNode("Reformat")
            reformat_node["type"].setValue("scale")
            reformat_node["scale"].setValue(0.5)
            reformat_node.setInput(0, read_node)

            # Write
            write_node = nuke.createNode("Write")
            write_node["file"].fromUserText(self.render_path_proxy)
            write_node["file_type"].setValue("mov")  # Establecer el tipo de archivo a MOV
            write_node["mov64_codec"].setValue("h264")  # Establecer el códec a H.264
            write_node["mov64_quality"].setValue("Low")  # Establecer la calidad a baja
            write_node["proxy"].fromUserText(self.render_path_proxy)
            knob = write_node['colorspace']

            for i in range(knob.numValues()):
                option_name = knob.enumName(i)
                if "sRGB" in option_name:
                    knob.setValue(i)
                    break

            write_node.setInput(0, reformat_node)
            read_node["reload"].execute()
            nuke.root()['proxy'].setValue(False)
            nuke.execute(write_node, continueOnError=True)

        nuke.delete(group)