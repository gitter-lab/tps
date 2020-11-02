import os
import subprocess


class Parser:
    def __init__(self, params):
        self.params = params

    def parse(self):

        '''
        - parse input config file 
        - build TPS call 
        - call TPS 
        - gather outputs 
        - return:
            - list of outputs 
            - output_folder
            - out_label

      
        '''
        # # grab TPS self.params 
        build = []
        OUT_FOLDER = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        OUT_LABEL = ""

        # add TPS run call as first arg
        build.extend(["bash", "./scripts/run"])

        # grab self.params from config
        req = self.params[1]["TPS"][0]["required"]
        op = self.params[1]["TPS"][1]["optional"]

        # filter given args
        filtered = {**req, **op}
        args = {key:val for key, val in filtered.items() 
                if filtered[key] != ""}

                    
        for key, val in args.items():
            if key == "outlabel":
                OUT_LABEL = str(val)
            if key == "outfolder":
                OUT_FOLDER = os.path.abspath(val)
            if val == "1":
                build.extend(['--' + key])
            else:
                k = "--" + key
                build.extend([k, str(val)])

 
        print("outfolder switch {}".format(OUT_FOLDER))
        print("OUTLABEL: ", OUT_LABEL)

        process = subprocess.run(
            build,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        # check output 

        outputs = str(subprocess.check_output(["ls", "-d", str(OUT_LABEL)+"*"], cwd=OUT_FOLDER), encoding= "utf-8").strip().split()

        outputs.append(OUT_LABEL)

        return outputs, OUT_FOLDER, OUT_LABEL