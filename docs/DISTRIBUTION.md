# Guía de Distribución (Winget & Homebrew)

Al hacer un "Release" o empujar un "Tag" a GitHub, GitHub Actions compilará ejecutables independientes (`llama-forge-manager.exe` para Windows, `llama-forge-manager-linux` para Ubuntu y `llama-forge-manager-macos` para Mac) y los adjuntará al Release.

A partir de esos binarios precompilados, puedes publicarlos en repositorios globales siguiendo esta guía.

---

## 1. Publicar en Winget (Windows)

Para que el comando `winget install llama-forge` funcione de forma oficial:

1. Crea un _Fork_ del repositorio oficial de Microsoft: [microsoft/winget-pkgs](https://github.com/microsoft/winget-pkgs)
2. Descarga la herramienta `wingetcreate` de la Microsoft Store o usando winget: `winget install wingetcreate`.
3. Ejecuta el asistente de creación en la consola pasando el link directo al archivo `.exe` del GitHub Release de tu proyecto:
   ```bash
   wingetcreate new https://github.com/JordanTX21/llama-forge-manager/releases/download/v1.0.0/llama-forge-manager.exe
   ```
4. El asistente generará los manifiestos YAML interactuando contigo (pedirá el nombre del autor, licencia, versión, etc.).
5. Una vez generados, usa el comando de submit de la misma herramienta o envía el Pull Request manualmente a tu fork de `winget-pkgs`.
6. En un plazo de unos días, Microsoft aprobará el PR y la app será instalable por cualquiera en Windows.

---

## 2. Publicar en Homebrew (macOS / Linux)

Brew utiliza el concepto de _Taps_ (repositorios adicionales). Al no estar inicialmente en el core de Brew, los usuarios instalarán la app desde tu propio _Tap_.

1. Crea un nuevo repositorio público en GitHub llamado `homebrew-llama-forge`.
2. En ese repositorio, crea un archivo llamado `llama-forge.rb` con el siguiente contenido:

```ruby
class LlamaForge < Formula
  desc "Local AI Manager for Llama.cpp and Llama-swap"
  homepage "https://github.com/JordanTX21/llama-forge-manager"

  if OS.mac?
    url "https://github.com/JordanTX21/llama-forge-manager/releases/download/v1.0.0/llama-forge-manager-macos"
    sha256 "REEMPLAZAR_CON_EL_SHA256_DEL_ARCHIVO_MAC"
  elsif OS.linux?
    url "https://github.com/JordanTX21/llama-forge-manager/releases/download/v1.0.0/llama-forge-manager-linux"
    sha256 "REEMPLAZAR_CON_EL_SHA256_DEL_ARCHIVO_LINUX"
  end

  version "1.0.0"

  def install
    if OS.mac?
      bin.install "llama-forge-manager-macos" => "llama-forge"
    elsif OS.linux?
      bin.install "llama-forge-manager-linux" => "llama-forge"
    end
  end

  test do
    # Verifica que el comando funciona (llama-forge) o falla controladamente y no con un error binario.
    system "#{bin}/llama-forge", "--help"
  end
end
```

### Instrucciones para tus Usuarios de macOS/Linux:

En el README de tu proyecto principal, deberás decirles a tus usuarios que ejecuten:

```bash
brew tap TU_USUARIO/llama-forge
brew install llama-forge
```

Y luego simplemente podrán ejecutar `llama-forge` en su terminal para levantar el panel.
