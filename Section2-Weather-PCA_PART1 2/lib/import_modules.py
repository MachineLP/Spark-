import importlib
import sys
modules=[('pandas','pd','0.19.2'),
('numpy','np','1.12.0'),
('sklearn','sk','0.18.1'),
('urllib','urllib','1.17'),
('pyspark','pyspark','2.1.0'),
('ipywidgets','ipywidgets','6.0.0')
]

def import_modules(modules,Unknown_versions=False):
    for module in modules:
        if Unknown_versions:
            name,shortname=module
        else:
            name,shortname,req_version=module

        try:
            globals()[shortname]=importlib.import_module(name)
            version=globals()[shortname].__version__
            if Unknown_versions:
                print("('%s','%s','%s'),"%(name,shortname,version))
            else:
                print("%10s as %5s \tversion=%s \trequired version>=%s"%(name,shortname,version,req_version),)
                if version<req_version:
                    print('******* Update Version ******')
                else:
                    print(
)
        except AttributeError:
            print('module %s has no version'%name)
        except:
            print(sys.exc_info())
            print('***** Failed to load module %s *******'%name)