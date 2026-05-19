import requests
import os

# Requisito de la rúbrica: Leer variables de entorno (aunque PokeAPI sea libre, demostramos el uso de os)
api_key_dummy = os.getenv('API_KEY_PROYECTO', 'sin_llave_necesaria')

def consultar_pokemon(nombre):
    url = f"https://pokeapi.co/api/v2/pokemon/{nombre}"
    
    try:
        # 1. Manejo de Timeout (Error 1)
        respuesta = requests.get(url, timeout=5)
        
        # 2. Manejo de recurso no encontrado (Error 2)
        if respuesta.status_code == 404:
            print(f"❌ Error 404: El Pokémon '{nombre}' no existe en la Pokédex o está mal escrito.")
            return
            
        # 3. Manejo de código inesperado (Error 3)
        elif respuesta.status_code != 200:
            print(f"⚠️ Error del servidor: código inesperado {respuesta.status_code}")
            return
            
        # Procesamiento exitoso de >= 3 campos de datos
        datos = respuesta.json()
        stats = {s["stat"]["name"]: s["base_stat"] for s in datos["stats"]}
        tipo = datos["types"][0]["type"]["name"]
        
        print(f"\n=== ANÁLISIS DE STATS: {datos['name'].upper()} ===")
        print(f"Tipo base : {tipo.capitalize()}")
        print(f"HP        : {stats.get('hp', '?')}")
        print(f"Ataque    : {stats.get('attack', '?')}")
        print(f"Velocidad : {stats.get('speed', '?')}")
        print("=======================================")

    # 4. Manejo de falta de conexión a internet (Error 4)
    except requests.exceptions.ConnectionError:
        print("🔌 Error de Red: Sin conexión. Verifica tu internet e inténtalo de nuevo.")
    except requests.exceptions.Timeout:
        print("⏱️ Error de Timeout: El servidor tardó más de 5 segundos. Inténtalo de nuevo.")

if __name__ == "__main__":
    print("--- Analizador Táctico de Pokémon ---")
    poke_input = input("Ingresa el nombre del Pokémon para analizar sus stats base: ").strip().lower()
    
    if poke_input:
        consultar_pokemon(poke_input)
    else:
        print("Entrada vacía. Finalizando programa.")