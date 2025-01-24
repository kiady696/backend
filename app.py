from flask import Flask, render_template
import pkg_resources

devmode = True

app = Flask(__name__,
        static_folder = "../frontend/dist/assets",
        template_folder = "../frontend/dist")



@app.route('/')
def homepage():
    return render_template('index.html')

@app.route('/api/python_pkg')
def pkg():
    installed_packages = pkg_resources.working_set
    installed_packages_list = sorted(["%s  %s" % (i.key, i.version) for i in installed_packages])
    return installed_packages_list


@app.route('/api/mode')
def getMode():
    return {"devmode":devmode}


if __name__ == '__main__':
    app.run(port=4000,debug=devmode)