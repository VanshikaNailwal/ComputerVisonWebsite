import importlib.util




def load_logic(logic_path):


    try:


        spec = importlib.util.spec_from_file_location(

            "logic_module",

            logic_path

        )



        logic_module = importlib.util.module_from_spec(

            spec

        )



        spec.loader.exec_module(

            logic_module

        )



        return logic_module




    except Exception as e:


        print(
            "Logic loading failed:",
            e
        )


        return None