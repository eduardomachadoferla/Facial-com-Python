import subprocess


def falar(texto):

    try:

        texto = texto.replace(
            "'",
            "''"
        )

        comando = (
            "Add-Type -AssemblyName System.Speech; "
            "$voz = New-Object "
            "System.Speech.Synthesis.SpeechSynthesizer; "
            f"$voz.Speak('{texto}')"
        )

        subprocess.Popen(
            [
                "powershell",
                "-NoProfile",
                "-Command",
                comando
            ]
        )

    except Exception:

        print(texto)