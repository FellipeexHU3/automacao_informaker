import pyautogui
import time

def coordenadas():
    print("🎯 COORDENADAS REAIS DO SEU MONITOR")
    print("=" * 40)
    print("Resolução: 1366x768")
    print("Escala: 100%")
    print("\n📍 Mova o mouse e veja as coordenadas")
    print("💡 As coordenadas DEVEM estar entre:")
    print("   X: 0 a 1366")
    print("   Y: 0 a 768")
    print("\n❌ Se aparecer acima disso, tem algo errado!")
    print("⏺️ Pressione Ctrl+C para parar")

    try:
        while True:
            x, y = pyautogui.position()
            print(f"X: {x:4d} | Y: {y:4d} | (Máx: X=1366, Y=768)", end='\r')
            time.sleep(0.1)
    except KeyboardInterrupt:
        print(f"\n\n✅ Coordenadas finais: X={x}, Y={y}")