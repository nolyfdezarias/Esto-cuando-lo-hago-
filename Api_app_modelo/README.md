# Modelos de optimizacion. 

### Pasos para recrear el entorno de test

1. Crear y activar entorno virtual de python
'python -m venv my-venv'
'source my-venv/bin/activate'

2. Instalar las dependencias necesarias en el entorno:
'pip install -r requirements.txt'

3. Crear hostpot con el movil y conectar la PC. Determinar IP que asume la PC en la conexion
'ipconfig' en windows
'ifconfig' en linux

4. ejecutar 'python app.py' en el directorio raiz. (Levantar API, notar que lo hace en el puerto 5000 por defecto)

5. Abrir la apk previamente instalada e introducir el IP de la maquina seguida del puerto 5000. Esta sera la direccion base de todas las peticiones requeridas para el correcto funcionamiento de la aplicacion.




