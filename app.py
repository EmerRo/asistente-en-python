import multiprocessing
import os
import psutil
import speech_recognition as sr
import pyttsx3

def obtener_informacion():
  cpu_uso = psutil.cpu_percent(interval=1)
  ram_uso = psutil.virtual_memory().percent
  disk_uso = psutil.disk_usage('/').percent
  informacion =f"Uso de CPU: {cpu_uso}%\n Uso de RAM:{ram_uso}%\n Uso de disco:{disk_uso}%"
  return informacion
def abrir_aplicacion(aplicacion):   
  try:
    if aplicacion.lower() == "google":
     os.system("start chrome")
    elif aplicacion.lower() == "calculadora":
     os.system("start calc")
    elif aplicacion.lower() == "excel":
     os.system("start excel")
    elif aplicacion.lower() == "word":
     os.system("start winword")
    else:
     return f"No se conoce la aplicacion {aplicacion}"
    return f"Abriendo {aplicacion}"
  except Exception as e:
   return f"No se pudo abrir {aplicacion}.Error:{str(e)}"

def reconocer_voz():
 recognizer= sr.Recognizer()
 with sr.Microphone() as source:
  print("Hablame...")
  recognizer.adjust_for_ambient_noise(source)
  audio = recognizer.listen(source)
                        
  try:
   texto= recognizer.recognize_google(audio, language="es-ES")
   print("Has dicho: " + texto)
   return texto.lower()    
  except sr.UnknownValueError:
   print("No se pudo entender el audio")
  except sr.RequestError as e:
   print("Error en la solicitud a Google Speech Recognition; {0}".format(e))

def hablar(texto):

 engine = pyttsx3.init()
 engine.say(texto)
 engine.runAndWait()      

def asistente():
 while True:
  comando = reconocer_voz()
  if 'terminar' in comando:
   print("Adios")
   hablar("Hasta luego")
   break
  elif 'hola' in comando:
   hablar("¡Hola! Rodrigo, soy tu asistente virtual")
  elif 'información' in comando:
   informacion_sistema = obtener_informacion()
   print(informacion_sistema)
   hablar(informacion_sistema)
  elif 'núcleos' in comando:
   cpu_count = multiprocessing.cpu_count()
   print(f"Hay {cpu_count} núcleos en tu computadora")
   hablar(f"Hay {cpu_count} núcleos en tu computadora")
  elif 'abrir' in comando:
   _, aplicacion = comando.split(" ", 1)
   resultado = abrir_aplicacion(aplicacion)
   print(resultado)
   hablar(resultado)
  else:
   hablar("No entiendo lo que quieres decir")

if __name__ == "__main__":
 proceso_asitente = multiprocessing.Process(target=asistente) 

 try :
  proceso_asitente.start()
  proceso_asitente.join()
 except KeyboardInterrupt:
  print("Proceso interrumpido. Adios.")
 finally:
  proceso_asitente.terminate()