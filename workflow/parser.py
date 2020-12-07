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
        print("=================================================")
        print("START PARSING CONFIG")

        
        # # grab TPS self.params 
        build = []
        OUT_FOLDER = ""
        OUT_LABEL = ""
        OUT_FOLDER = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

        # add TPS run call as first arg
        build.extend(["bash", "./scripts/run"])

        # grab self.params from config
        req = self.params["TPS"]["required"]
        op = self.params["TPS"]["optional"]
        flags = self.params["TPS"]['flags']

        # filter given args
        filtered = {**req, **op}
        args = {key:val for key, val in filtered.items() 
                if filtered[key] != "None"}

        # grab out label (required)
        OUT_LABEL = args['outlabel']

        # check for out dir (optional)
        # list will contain one item if path provided, else empty list returned 
        check_outfolder = 'outfolder'
        if check_outfolder in args:
            OUT_FOLDER = args[check_outfolder]

        # build tps call 
        for key, val in args.items():
            k = "--" + key
            build.extend([k, str(val)])
        build.extend(flags)

        # debug statements 
        print("---outfolder switch {}".format(OUT_FOLDER))
        print("---OUTLABEL: ", OUT_LABEL)
        print("---tps build:")
        print(build)

        # run TPS 
        process = subprocess.run(
            build,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )

        # check output 
        outputs = str(subprocess.check_output(["ls", "-d", str(OUT_LABEL)+"*"], cwd=OUT_FOLDER), encoding= "utf-8").strip().split()

        for file in outputs:
            if not os.path.exists(file):
                raise Exception("output file {} was not generated, check TPS build".format(file))


        outputs.append(OUT_LABEL)

        return outputs, OUT_FOLDER, OUT_LABEL