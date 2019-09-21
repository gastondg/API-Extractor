import subprocess


if __name__ == "__main__":
    subprocess.run("ls -la", shell=True)
    # a = subprocess.run('env/bin/python3 prueba_lambda.py >> prueba.txt | at now', shell=True)
    # print(a)
    id_busqueda = 2
    subprocess.run('env/bin/python3 prueba_lambda.py ' + str(id_busqueda) + ' >> prueba.txt | at now', shell=True)
    