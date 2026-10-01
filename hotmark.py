# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#                                      Hotmart Course Downloader                                                      #
#                                                                                                                     #
#  Baseado no gist original de @juvenal: https://gist.github.com/juvenal/2d9a822325769d30c45c635fbf388c1b           #
#  Atualizado: Barra de Progresso em Tempo Real (0%-100%), Contagem Regressiva, Retomada e Compactador CRF            #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

import sys
import time
import datetime
import requests
import m3u8
import re
import os
import shutil
from bs4 import BeautifulSoup
import youtube_dl
import subprocess
import glob
import unicodedata

# ==============================================================================
# >>> [CONFIGURAÇÃO DO DIRETÓRIO DE DESTINO] <<<
# ==============================================================================
DIRETORIO_DESTINO = r"G:\Meu Drive\Alexandre\Guitarra Intensiva"

# ==============================================================================
# >>> [CONFIGURAÇÃO DO COMPACTADOR DE VÍDEO] <<<
# ==============================================================================
COMPACTAR_VIDEO = True        # True para ativar compactação; False para fluxo original
CODEC_VIDEO = "libx264"       # "libx264" (compatibilidade universal)
CRF_QUALIDADE = 22            # 20 a 23 = visualmente idêntico ao original
PRESET_VELOCIDADE = "faster"  # "faster" oferece ótimo equilíbrio entre tempo e compressão
# ==============================================================================

TOKEN_INICIAL = (
    "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9."
    "eyJqdGkiOiJUR1QtMTg1MS1yeFVZV09pck82QVhjVEZmOFM4bXFzUDNQdTdDUTJQczMtdVNPVUJkTFg4YnppOWtSS1pRN2VsTGpUbHdqcDI0clhVLWhvdC1zc28tNWQ3NThkNWM3ZC16dzVqZCIsInNpZCI6IjcxY2I2YjY1LWFhY2QtNDJhYi05OGI0LWZkODY4NjYxNmQyYSIsImlzcyI6Imh0dHBzOi8vc3NvLmhvdG1hcnQuY29tL29pZGMiLCJhdWQiOlsiZmI1ZTE4YmEtMjAzZi0xMWVhLTk3OGYtMmU3MjhjZTg4MTI1IiwiYjQzMmNkZDMtZWI2MC00NmJkLTg5MmItNWI0NTBhNjUxNTNlIl0sImV4cCI6MTc5MjA2MjcxNCwiaWF0IjoxNzkwODUyOTk2LCJuYmYiOjE3OTA4NTI2OTYsInN1YiI6IjgwNjMwNzIyIiwiYW1yIjpbIkRlbGVnYXRlZENsaWVudEF1dGhlbnRpY2F0aW9uSGFuZGxlciJdLCJjbGllbnRfaWQiOiJiNDMyY2RkMy1lYjYwLTQ2YmQtODkyYi01YjQ1MGE2NTE1M2UiLCJhdXRoX3RpbWUiOjE3OTA4NTI5OTUsInN0YXRlIjoiMTk2NTg3ZmU0ZTUwNGU0NGE1ZDNiZmY3MTY0YjVhMGIiLCJhdF9oYXNoIjoiY21CcklqY1owVU9lSV9oTF9wRVJnQSIsImFkZHJlc3MiOnsiY291bnRyeSI6IkJyYXNpbCIsImlkIjo5NTY2OTkzNn0sImFkZHJlc3NDb3VudHJ5IjoiQnJhc2lsIiwiYWRkcmVzc0lkIjo5NTY2OTkzNiwiYXV0aG9yaXRpZXMiOlsibm9fcm9sZSIsImNvbXByYWRvciIsInVzZXJfYnIiXSwiY3VycmVuY3lDb2RlQ29taXNzaW9uIjoiVVNEIiwiZW1haWwiOiJwcm9mLmFsZXhhbmRyZXNhdHlyb0BnbWFpbC5jb20iLCJlbnRpdHlUeXBlIjoiSU5ESVZJRFVBTF9FTlRJVFkiLCJpZCI6IjgwNjMwNzIyIiwibG9jYWxlIjoiUFRfQlIiLCJsb2dpbiI6InByb2ZhbGV4YW5kcmVzYXR5cm8iLCJsb2dpbkF0dGVtcHRzIjowLCJuYW1lIjoiQUxFWEFORFJFIFNBVFlSTyBGT1JUVU5BVEkiLCJzaWdudXBEYXRlIjoxNzA5MjA5NDI5MDAwLCJzdGF0dXMiOiJBdGl2byIsInVjb2RlIjoiODBhMGE5YTktYzFhZC00MWY2LThmNzgtM2MyNjRmOGJjZTBkIiwicHJlZmVycmVkX3VzZXJuYW1lIjoiODA2MzA3MjIiLCJzY29wZSI6WyJ1c2VyIiwiYXV0aG9yaXRpZXMiLCJlbWFpbCIsIm9wZW5pZCIsInByb2ZpbGUiXSwiYWNjZXNzX3Rva2VuIjoiQVQtNjM1MC1vbVZSajE0ODEtR3dNbDdhd0ZOSjhnd2h5Unk5UERaLSJ9."
    "JlgKR0nRp2enHSbp0jcaUcZELqff2NA5FDyJWJcLdhZpB1FvRuMGFgzJi9FhpO7U67dJ-Bi_SqeeKZQhFCneCnq309pGHcMZwW888NIqFGPRpVDnAePHNVMXlAxcTyAQ7mTq808P--molJQULYIwiGRJUGzvy2qMDSmOim2OlF5BYfGETkY0laCL5LknItsVIH_ZAJuRpc6HJWRHR61_3N6LDXMv5ElhECwKjyQSGPn8k5opwmN2AfJD7rHnRU0d_Dav_n9ffw9YAwRLoKEoMvOXG0JrxkYVvclEMlIbvICB8ZNQiYcU55Piv6SBsL91lIIGWGTt8jZWkLdesqU9wg"
)

SLUG_CURSO = "rodrigoferrarezi"
PRODUCT_ID = "180527"


def formatar_tempo(segundos):
    segundos = max(0, int(segundos))
    m, s = divmod(segundos, 60)
    h, m = divmod(m, 60)
    if h > 0:
        return f"{h:02d}:{m:02d}:{s:02d}"
    return f"{m:02d}:{s:02d}"


def formatar_bytes(num_bytes):
    num = float(num_bytes)
    for unit in ['B', 'KB', 'MB', 'GB']:
        if abs(num) < 1024.0:
            return f"{num:.1f} {unit}"
        num /= 1024.0
    return f"{num:.1f} TB"


def obter_caminho_ffmpeg():
    if shutil.which("ffmpeg"):
        return "ffmpeg"
    try:
        import imageio_ffmpeg
        caminho = imageio_ffmpeg.get_ffmpeg_exe()
        if os.path.isfile(caminho):
            return caminho
    except ImportError:
        pass

    caminhos_playwright = glob.glob(os.path.expanduser(r"~\AppData\Local\ms-playwright\ffmpeg-*\ffmpeg-win64.exe"))
    if caminhos_playwright and os.path.isfile(caminhos_playwright[0]):
        return caminhos_playwright[0]

    if os.path.isfile("ffmpeg.exe"):
        return os.path.abspath("ffmpeg.exe")

    return "ffmpeg"


def slugify(value, allow_unicode=False):
    value = str(value)
    if allow_unicode:
        value = unicodedata.normalize('NFKC', value)
    else:
        value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore').decode('ascii')
    value = re.sub(r'[^\w\s-]', '', value.lower())
    return re.sub(r'[-\s]+', '-', value).strip('-_')


def mover_arquivo_seguro(origem, destino):
    if os.path.isfile(destino):
        try:
            os.remove(destino)
        except Exception:
            pass
    shutil.move(origem, destino)


def obter_duracao_m3u8(session, m3u8_url):
    """Calcula a duração total dos segmentos do arquivo m3u8 em segundos."""
    try:
        headers_m3u8 = {
            'Origin': 'https://cf-embed.play.hotmart.com',
            'Referer': 'https://cf-embed.play.hotmart.com/',
            'User-Agent': session.headers.get('user-agent', 'Mozilla/5.0')
        }
        r = session.get(m3u8_url, headers=headers_m3u8, timeout=10)
        if r.status_code == 200:
            playlist = m3u8.loads(r.text)
            if playlist.segments:
                return sum(float(s.duration) for s in playlist.segments if s.duration)
            elif playlist.playlists:
                sub_uri = playlist.playlists[0].uri
                if not sub_uri.startswith('http'):
                    base = m3u8_url.rsplit('/', 1)[0]
                    sub_uri = f"{base}/{sub_uri}"
                r_sub = session.get(sub_uri, headers=headers_m3u8, timeout=10)
                if r_sub.status_code == 200:
                    sub_playlist = m3u8.loads(r_sub.text)
                    if sub_playlist.segments:
                        return sum(float(s.duration) for s in sub_playlist.segments if s.duration)
    except Exception:
        pass
    return None


def executar_ffmpeg_com_progresso(cmd, total_segundos, rotulo="Progresso"):
    """Executa o FFmpeg e exibe porcentagem (0%-100%), contagem regressiva e tamanho na mesma linha."""
    cmd_exec = list(cmd)
    if '-progress' not in cmd_exec:
        cmd_exec.extend(['-progress', 'pipe:1', '-nostats'])

    process = subprocess.Popen(
        cmd_exec,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        universal_newlines=True,
        encoding='utf-8',
        errors='replace'
    )

    tempo_atual = 0.0
    tamanho_atual = 0
    velocidade = "1.0x"

    for line in process.stdout:
        line = line.strip()
        if not line or '=' not in line:
            continue
        k, v = line.split('=', 1)
        k = k.strip()
        v = v.strip()

        if k == 'out_time':
            parts = v.split(':')
            if len(parts) == 3:
                try:
                    tempo_atual = float(parts[0]) * 3600 + float(parts[1]) * 60 + float(parts[2])
                except ValueError:
                    pass
        elif k == 'total_size':
            try:
                tamanho_atual = int(v)
            except ValueError:
                pass
        elif k == 'speed':
            velocidade = v
        elif k == 'progress':
            if total_segundos and total_segundos > 0:
                pct = min(100.0, (tempo_atual / total_segundos) * 100.0)
                bar_len = 22
                filled = int(bar_len * (pct / 100.0))
                bar = '=' * filled + ('>' if filled < bar_len else '')
                bar = bar.ljust(bar_len)
                falta_seg = max(0, total_segundos - tempo_atual)
                sys.stdout.write(
                    f"\r    [{rotulo}] {pct:5.1f}% [{bar}] "
                    f"{formatar_tempo(tempo_atual)} / {formatar_tempo(total_segundos)} "
                    f"(Falta {formatar_tempo(falta_seg)}) | {formatar_bytes(tamanho_atual)} | {velocidade}   "
                )
            else:
                sys.stdout.write(
                    f"\r    [{rotulo}] {formatar_tempo(tempo_atual)} | "
                    f"{formatar_bytes(tamanho_atual)} | {velocidade}   "
                )
            sys.stdout.flush()

    process.wait()
    sys.stdout.write("\n")
    sys.stdout.flush()
    return process.returncode


def baixar_arquivo_com_progresso(url, destino_path, rotulo="Anexo", session=None):
    """Baixa arquivos via HTTP exibindo porcentagem, barra e contagem regressiva de MB."""
    req_mod = session if session else requests
    try:
        with req_mod.get(url, stream=True, timeout=60) as resp:
            resp.raise_for_status()
            total_size = int(resp.headers.get('content-length', 0))
            downloaded = 0
            chunk_size = 1024 * 64

            with open(destino_path, 'wb') as f:
                for chunk in resp.iter_content(chunk_size=chunk_size):
                    if chunk:
                        f.write(chunk)
                        downloaded += len(chunk)
                        if total_size > 0:
                            pct = (downloaded / total_size) * 100
                            bar_len = 22
                            filled = int(bar_len * (downloaded / total_size))
                            bar = '=' * filled + ('>' if filled < bar_len else '')
                            bar = bar.ljust(bar_len)
                            falta_bytes = max(0, total_size - downloaded)
                            sys.stdout.write(
                                f"\r    [{rotulo}] {pct:5.1f}% [{bar}] "
                                f"{formatar_bytes(downloaded)} / {formatar_bytes(total_size)} "
                                f"(Falta {formatar_bytes(falta_bytes)})   "
                            )
                        else:
                            sys.stdout.write(f"\r    [{rotulo}] Baixado: {formatar_bytes(downloaded)}   ")
                        sys.stdout.flush()
        sys.stdout.write("\n")
        sys.stdout.flush()
        return os.path.isfile(destino_path) and os.path.getsize(destino_path) > 0
    except Exception as e:
        sys.stdout.write(f"\n    [ERRO] Falha no download: {e}\n")
        return False


def extrair_google_drive_urls(html_content):
    if not html_content:
        return []
    urls = []
    pattern = r'drive\.google\.com/file/d/([a-zA-Z0-9_-]+)'
    matches = re.findall(pattern, html_content)
    for file_id in matches:
        preview_url = f"https://drive.google.com/file/d/{file_id}/preview"
        download_url = f"https://drive.google.com/uc?export=download&id={file_id}"
        urls.append((file_id, preview_url, download_url))
    return urls


def baixar_google_drive(file_id, download_url, output_path):
    try:
        session = requests.Session()
        response = session.get(download_url, stream=True)

        if 'confirm' in response.text or 'virus scan warning' in response.text.lower():
            soup = BeautifulSoup(response.text, 'html.parser')
            for link in soup.find_all('a'):
                href = link.get('href', '')
                if 'export=download' in href and 'confirm' in href:
                    download_url = 'https://drive.google.com' + href
                    break

        return baixar_arquivo_com_progresso(download_url, output_path, rotulo="GDrive", session=session)
    except Exception:
        return False


def criar_sessao_autenticada(token, slug, product_id):
    if not os.path.exists('temp'):
        os.makedirs('temp')
    for f in glob.glob("temp/*"):
        try:
            os.remove(f)
        except Exception:
            pass

    session = requests.session()
    session.headers.update({
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'pt-BR,pt;q=0.9,en;q=0.8',
        'authorization': f'Bearer {token}',
        'origin': 'https://hotmart.com',
        'referer': 'https://hotmart.com/',
        'slug': str(slug),
        'x-product-id': str(product_id),
        'x-app-name': 'app-club-consumer_v1.366.2_production',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    })
    return session


def renovar_token_se_necessario(session):
    print("\n" + "!" * 60)
    print(">>> SESSÃO EXPIRADA (HTTP 401/403) <<<")
    print("Copie o token mais recente no navegador.")
    print("!" * 60)
    novo_token = input("Cole o access_token atualizado aqui: ").strip()
    novo_token = novo_token.replace('"', '').replace("'", '').replace("Bearer ", "").strip()
    if novo_token:
        session.headers['authorization'] = f'Bearer {novo_token}'
        print("[OK] Token renovado na sessão! Retomando...\n")
        return True
    return False


def obter_dados_da_aula(session, page_obj, product_id):
    cod = page_obj.get('hash') or page_obj.get('id') or page_obj.get('code')
    if not cod:
        return {}

    rotas = [
        f'https://api-club.hotmart.com/hot-club-api/rest/v3/page/{cod}',
        f'https://api-club-course-consumption-gateway-ga.cb.hotmart.com/v1/pages/{cod}',
        f'https://api-club-course-consumption-gateway-ga.cb.hotmart.com/v1/content/{cod}'
    ]

    for url in rotas:
        try:
            resp = session.get(url, timeout=12)
            if resp.status_code == 200:
                return resp.json()
            elif resp.status_code in (401, 403):
                if renovar_token_se_necessario(session):
                    resp_retry = session.get(url, timeout=12)
                    if resp_retry.status_code == 200:
                        return resp_retry.json()
        except Exception:
            continue

    return {}


def obter_url_m3u8_assinada(session, vid):
    media_url = vid.get('mediaSrcUrl')
    video_hash = vid.get('mediaCode')

    candidatos = []
    if media_url:
        candidatos.append(media_url)
    if video_hash:
        candidatos.append(f"https://cf-embed.play.hotmart.com/v2/?videoCode={video_hash}")
        candidatos.append(f"https://play.hotmart.com/embed/{video_hash}")

    headers_leitor = {
        'Origin': 'https://hotmart.com',
        'Referer': 'https://hotmart.com/',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }

    for url in candidatos:
        try:
            resp = session.get(url, headers=headers_leitor, timeout=15)
            if resp.status_code == 200:
                texto = resp.text.replace(r'\/', '/').replace('&', '&').replace(r'\u0026', '&')
                links = re.findall(r'https?://[^\s"\'<>]+\.m3u8[^\s"\'<>]*', texto)
                for l in links:
                    if 'master' in l or (video_hash and video_hash in l) or 'vod-' in l:
                        return l
                if links:
                    return links[0]
            elif resp.status_code in (401, 403):
                renovar_token_se_necessario(session)
        except Exception:
            continue

    return None


def baixar_video_hotmart(session, vid, pasta_aula, idx_v, ffmpeg_bin):
    video_local_path = os.path.join(pasta_aula, f"aula-{slugify(str(idx_v))}.mp4")
    video_temp_raw = os.path.join("temp", f"raw_{vid.get('mediaCode')}.mp4")
    video_temp_part = os.path.join(pasta_aula, f"aula-{slugify(str(idx_v))}.part.mp4")

    # [VERIFICAÇÃO DE RETOMADA]
    if os.path.isfile(video_local_path):
        tamanho = os.path.getsize(video_local_path)
        if tamanho > 100 * 1024:
            mb = tamanho / (1024 * 1024)
            print(f"  [CONCLUÍDO - PULANDO] Vídeo {idx_v} íntegro ({mb:.1f} MB)")
            return True
        else:
            print(f"  [AVISO] Arquivo corrompido detectado ({tamanho} bytes). Rebaixando...")
            try:
                os.remove(video_local_path)
            except Exception:
                pass

    for lixo in [video_temp_raw, video_temp_part]:
        if os.path.isfile(lixo):
            try:
                os.remove(lixo)
            except Exception:
                pass

    print(f"  [HOTMART] A localizar fluxo do vídeo {idx_v} (Código: {vid.get('mediaCode')})...")
    m3u8_url = obter_url_m3u8_assinada(session, vid)

    if not m3u8_url:
        print("  [ERRO] Não foi possível obter a URL m3u8 assinada.")
        return False

    total_segundos = obter_duracao_m3u8(session, m3u8_url)
    duracao_txt = f" ({formatar_tempo(total_segundos)})" if total_segundos else ""
    print(f"  [ETAPA 1/2] Baixando fluxo de vídeo original{duracao_txt}...")

    headers_ffmpeg = (
        "Origin: https://cf-embed.play.hotmart.com\r\n"
        "Referer: https://cf-embed.play.hotmart.com/\r\n"
        "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36\r\n"
    )

    cmd_download = [
        ffmpeg_bin,
        '-hide_banner',
        '-loglevel', 'error',
        '-headers', headers_ffmpeg,
        '-i', m3u8_url,
        '-c', 'copy',
        '-bsf:a', 'aac_adtstoasc',
        '-f', 'mp4',
        video_temp_raw
    ]

    ret = executar_ffmpeg_com_progresso(cmd_download, total_segundos, rotulo="Baixando Vídeo")

    if ret != 0 or not os.path.isfile(video_temp_raw) or os.path.getsize(video_temp_raw) < 100 * 1024:
        print("  [PROCESSANDO] Tentando download via transcodificação direta...")
        cmd_fallback = [
            ffmpeg_bin,
            '-hide_banner',
            '-loglevel', 'error',
            '-headers', headers_ffmpeg,
            '-i', m3u8_url,
            '-preset', 'ultrafast',
            '-f', 'mp4',
            video_temp_raw
        ]
        executar_ffmpeg_com_progresso(cmd_fallback, total_segundos, rotulo="Download (Fallback)")

    if not os.path.isfile(video_temp_raw) or os.path.getsize(video_temp_raw) < 100 * 1024:
        print("  [ERRO] Falha no download do fluxo de vídeo.")
        return False

    # [ETAPA 2: COMPACTAÇÃO LOCAL]
    tamanho_original = os.path.getsize(video_temp_raw)
    mb_original = tamanho_original / (1024 * 1024)

    if COMPACTAR_VIDEO:
        print(f"  [ETAPA 2/2] Otimizando tamanho (CRF {CRF_QUALIDADE} | {CODEC_VIDEO} | Áudio 100% original)...")
        cmd_compress = [
            ffmpeg_bin,
            '-hide_banner',
            '-loglevel', 'error',
            '-i', video_temp_raw,
            '-c:v', CODEC_VIDEO,
            '-crf', str(CRF_QUALIDADE),
            '-preset', PRESET_VELOCIDADE,
            '-c:a', 'copy',
            '-f', 'mp4',
            video_temp_part
        ]
        ret_cmp = executar_ffmpeg_com_progresso(cmd_compress, total_segundos, rotulo="Compactando")

        if ret_cmp == 0 and os.path.isfile(video_temp_part) and os.path.getsize(video_temp_part) > 100 * 1024:
            mover_arquivo_seguro(video_temp_part, video_local_path)
            tamanho_final = os.path.getsize(video_local_path)
            mb_final = tamanho_final / (1024 * 1024)
            economia = (1 - (tamanho_final / tamanho_original)) * 100
            print(f"  [OK] Concluído: {mb_original:.1f} MB -> {mb_final:.1f} MB ({economia:.1f}% menor)")
        else:
            mover_arquivo_seguro(video_temp_raw, video_local_path)
            print(f"  [AVISO] Compressão falhou. Arquivo original salvo ({mb_original:.1f} MB).")
    else:
        mover_arquivo_seguro(video_temp_raw, video_local_path)
        print(f"  [OK] Vídeo salvo sem compactação ({mb_original:.1f} MB).")

    for lixo in [video_temp_raw, video_temp_part]:
        if os.path.isfile(lixo):
            try:
                os.remove(lixo)
            except Exception:
                pass

    return True


def baixar_curso(session, first_folder, slug, product_id):
    if not os.path.exists(first_folder):
        os.makedirs(first_folder, exist_ok=True)

    ffmpeg_bin = obter_caminho_ffmpeg()
    print(f"[FFMPEG] Binário configurado: {ffmpeg_bin}")

    print(f"\n[INFO] Acedendo ao curso (Slug: {slug}, Produto: {product_id})...")
    nav_url = 'https://api-club-course-consumption-gateway-ga.cb.hotmart.com/v1/navigation'
    response = session.get(nav_url)

    if response.status_code in (401, 403):
        if renovar_token_se_necessario(session):
            response = session.get(nav_url)

    if response.status_code != 200:
        print(f"\n[ERRO] Não foi possível carregar o navigation (HTTP {response.status_code}).")
        return

    dados_curso = response.json()
    modulos = dados_curso.get('modules') or dados_curso.get('data', {}).get('modules', [])

    if not modulos:
        print("\n[ERRO] Nenhum módulo encontrado na resposta.")
        return

    total_aulas_geral = sum(len(m.get('pages', [])) for m in modulos)
    print(f"[OK] Grade carregada! Total: {len(modulos)} módulos com {total_aulas_geral} aulas.\n")

    aula_cont = 0
    for modulo in modulos:
        mod_nome = re.sub(r'[<>:"/\\|?*]', '', modulo.get('name', 'Modulo')).strip()
        mod_ordem = modulo.get('moduleOrder', 0)
        pasta_modulo = os.path.join(first_folder, f"{slugify(str(mod_ordem))}_{slugify(mod_nome)}")
        os.makedirs(pasta_modulo, exist_ok=True)

        for p in modulo.get('pages', []):
            aula_cont += 1
            num_aula = p.get('pageOrder', 0)
            nome_aula = re.sub(r'[<>:"/\\|?*]', '', p.get('name', 'Sem Titulo')).strip()
            pasta_aula = os.path.join(pasta_modulo, f"{slugify(str(num_aula))}.{slugify(nome_aula)}")
            os.makedirs(pasta_aula, exist_ok=True)

            print(f"[{aula_cont}/{total_aulas_geral}] Verificando: {mod_nome} > {num_aula}. {nome_aula}")

            page_data = obter_dados_da_aula(session, p, product_id)

            conteudo_html = page_data.get('content', '')
            videos = page_data.get('mediasSrc', [])
            anexos = page_data.get('attachments', [])
            links = page_data.get('complementaryReadings', [])

            # Descrição em HTML
            desc_path = os.path.join(pasta_aula, "descricao.html")
            if conteudo_html and not os.path.isfile(desc_path):
                with open(desc_path, 'w', encoding='utf-8') as dd:
                    dd.write(str(conteudo_html))

            # 1. Download de Vídeos Nativos com Barra de Progresso
            if videos:
                for idx_v, vid in enumerate(videos, start=1):
                    baixar_video_hotmart(session, vid, pasta_aula, idx_v, ffmpeg_bin)

            # 2. Download de Vídeos Externos (YouTube / Vimeo)
            if not videos and conteudo_html:
                try:
                    soup = BeautifulSoup(conteudo_html, features="html.parser")
                    for idx_ext, iframe in enumerate(soup.find_all("iframe"), start=1):
                        src = iframe.get("src", "")
                        link_v = None
                        if 'player.vimeo' in src or 'vimeo.com' in src:
                            youtube_dl.utils.std_headers['Referer'] = 'https://hotmart.com/'
                            link_v = src.split('?')[0] if 'player.vimeo' in src else f"https://player.vimeo.com/video/{src.split('vimeo.com/')[1].split('?')[0]}"
                        elif "youtube.com" in src or "youtu.be" in src:
                            link_v = src

                        if link_v:
                            video_ext_path = os.path.join(pasta_aula, f"aula-{slugify(str(idx_ext))}.mp4")
                            video_ext_part = os.path.join(pasta_aula, f"aula-{slugify(str(idx_ext))}.part.mp4")

                            if os.path.isfile(video_ext_path) and os.path.getsize(video_ext_path) > 100 * 1024:
                                print(f"  [CONCLUÍDO - PULANDO] Vídeo externo já existe: aula-{idx_ext}.mp4")
                            else:
                                if os.path.isfile(video_ext_part):
                                    try:
                                        os.remove(video_ext_part)
                                    except Exception:
                                        pass
                                print(f"  [EXTERNO] Baixando: {link_v}")
                                ydl_opts = {"format": "best", 'outtmpl': video_ext_part}
                                with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                                    ydl.download([link_v])
                                if os.path.isfile(video_ext_part) and os.path.getsize(video_ext_part) > 0:
                                    mover_arquivo_seguro(video_ext_part, video_ext_path)
                except Exception as e:
                    print(f"  [AVISO] Erro em vídeo externo: {e}")

            # 3. Download de Anexos com Barra de Progresso
            pasta_materiais = os.path.join(pasta_aula, "Materiais")
            if anexos:
                os.makedirs(pasta_materiais, exist_ok=True)
                for anexo in anexos:
                    anexo_id = anexo.get('fileMembershipId')
                    anexo_nome = re.sub(r'[<>:"/\\|?*]', '', anexo.get('fileName', 'anexo')).strip()
                    anexo_path = os.path.join(pasta_materiais, anexo_nome)
                    anexo_part = os.path.join(pasta_materiais, f"{anexo_nome}.part")

                    if os.path.isfile(anexo_path) and os.path.getsize(anexo_path) > 0:
                        continue

                    if os.path.isfile(anexo_part):
                        try:
                            os.remove(anexo_part)
                        except Exception:
                            pass

                    print(f"  [ANEXO] Baixando: {anexo_nome}...")
                    try:
                        resp_anexo = session.get(f'https://api-club.hotmart.com/hot-club-api/rest/v3/attachment/{anexo_id}/download', timeout=30)
                        if resp_anexo.status_code == 200:
                            dl_url = resp_anexo.json().get('directDownloadUrl')
                            if dl_url:
                                if baixar_arquivo_com_progresso(dl_url, anexo_part, rotulo="Anexo"):
                                    mover_arquivo_seguro(anexo_part, anexo_path)
                                    print(f"  [OK] Anexo guardado: {anexo_nome}")
                    except Exception as e:
                        print(f"  [ERRO] Falha no anexo {anexo_nome}: {e}")

            # 4. Downloads do Google Drive com Barra de Progresso
            if conteudo_html:
                gdrive_files = extrair_google_drive_urls(conteudo_html)
                if gdrive_files:
                    os.makedirs(pasta_materiais, exist_ok=True)
                    for file_id, _, dl_url in gdrive_files:
                        gdrive_path = os.path.join(pasta_materiais, f"gdrive_{file_id}.pdf")
                        gdrive_part = os.path.join(pasta_materiais, f"gdrive_{file_id}.pdf.part")

                        if os.path.isfile(gdrive_path) and os.path.getsize(gdrive_path) > 0:
                            continue

                        if os.path.isfile(gdrive_part):
                            try:
                                os.remove(gdrive_part)
                            except Exception:
                                pass

                        print(f"  [GDRIVE] Baixando PDF Google Drive: {file_id}...")
                        if baixar_google_drive(file_id, dl_url, gdrive_part):
                            mover_arquivo_seguro(gdrive_part, gdrive_path)

            # 5. Leituras Complementares
            if links:
                os.makedirs(pasta_materiais, exist_ok=True)
                links_path = os.path.join(pasta_materiais, "links.txt")
                if not os.path.isfile(links_path):
                    with open(links_path, "a", encoding="utf-8") as lz:
                        for lk in links:
                            lz.write(f"{lk.get('articleName')}: {lk.get('articleUrl')}\n")

    print("\n" + "=" * 60)
    print("DOWNLOAD CONCLUÍDO COM SUCESSO!")
    print(f"Todos os arquivos estão em: {first_folder}")
    print("=" * 60)


if __name__ == "__main__":
    sessao = criar_sessao_autenticada(
        token=TOKEN_INICIAL,
        slug=SLUG_CURSO,
        product_id=PRODUCT_ID
    )
    baixar_curso(
        session=sessao,
        first_folder=DIRETORIO_DESTINO,
        slug=SLUG_CURSO,
        product_id=PRODUCT_ID
    )