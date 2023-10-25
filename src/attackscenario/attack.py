import paramiko
import getpass
import time
import os
from subprocess import Popen, PIPE
import re
import pandas as pd
import sys
# SSH connection details


jump_host = 'raspberrypi.local'
port = 22
username = 'darraghconnaughton'
password = getpass.getpass("Enter SSH password....")
TRACES = 5
target_host = '192.168.4.19'

URLS = [
    "3IosA_ir06Y",
    "bhpTZOqXRN0",
    "agTMr9qITlI",
    "sFEYQMrWNHU",
    "KUXS5fJPFSA",
    "BuwLLUzp7DI",
    "xYcHxF_cO8o",
    "ZI9Fjo8k618",
    "beHTyPTJzlQ",
    "JZ1ZoR0Y4SU",
    # "WAfJpyBgcgA",
    # "aQDXXSh1psg",
    # "cicNiSBsDGI",
    # "xF_lJGizHOY",
    # "WwAkT9Wk9Gk",
    # "wqGLislwe2M",
    # "ECnC3Meyff4",
    # "buVYv-3f2Kc",
    # "b7v5XDJrH5g",
    # "RvrSoAzXVsE",
    # "tmlMwjkShLE",
    # "sQn_tYguBIY",
    # "i8UNGbSHv6U",
    # "3rzyq9SH3Qw",
    # "EMm_34CoDRo",
    # "xLKoTS90pvQ",
    # "2IFYt20QON8",
    # "9A_YXyZb9VE",
    # "c5gRjiHdnLk",
    # "ABBHqDKHqoY",
    # "yxAm9uRuItI",
    # "0mm05SkR_Ys",
    # "sIGVmChnbI8",
    # "7GGzc3x9WJU",
    # "k1Do5KcJLYQ",
    # "fATegRW2EE4",
    # "XX5M6AvInLc",
    # "q_8_KvcVTFA",
    # "hDYFBB68NSk",
    # "Y2pVetbsK8g",
    # "XMEg6mfTfF4",
    # "UJl911UBoxg",
    # "j7K03oOhe9o",
    # "zovrM0LdrZ0",
    # "ik7_jZ8GL0g",
    # "BKLZT66P68A",
    # "SIajjK7jj2o",
    # "FzaSsoe2fpg",
    # "lQsjT42cQs4",
    # "RvxefSebjYE"
]

def establish_ssh_session(process_id, URI):
    # ===========
    # ===========
    # ===========
    # Create an SSH client for the jump host
    jump_client = paramiko.SSHClient()
    jump_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    # Connect to the jump host
    jump_client.connect(jump_host, port, username, password)

    # Create an SSH client for the target host
    target_transport = jump_client.get_transport()
    target_dest_addr = (target_host, port)
    target_local_addr = ('localhost', 0)  # Let the system choose a free port
    target_channel = target_transport.open_channel(
        "direct-tcpip", target_dest_addr, target_local_addr
    )
    # ===========
    # ===========
    # ===========

    # Create an SSH client for the target host using the tunnel
    target_client = paramiko.SSHClient()
    target_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    # Use the tunnel to connect to the target host
    target_client.connect(target_host, port, username, password, sock=target_channel)

    chan = target_client.get_transport().open_session()
    chan.setblocking(0)

    command_txt = f'/home/darraghconnaughton/attackscenario/venv/bin/python3 /home/darraghconnaughton/attackscenario/victim_viewer.py -n {URI}'
    print(f"[+]command: {command_txt}")
    chan.exec_command(command_txt)
    
    outdata, errdata = '', ''
    while True:  # monitoring process
        # Reading from output streams
        while chan.recv_ready():
            outdata += str(chan.recv(1000).decode("utf-8")) + "\n"
        while chan.recv_stderr_ready():
            errdata += str(chan.recv_stderr(1000).decode("utf-8")) + "\n"
        if chan.exit_status_ready():  # If completed
            break

    retcode = chan.recv_exit_status()

    match = re.search(r"'start': (\S+)}", outdata)
    start_time = float(match.group(1).strip())

    # Close the SSH clients and tunnel
    target_channel.close()
    target_client.close()
    jump_client.close()

    return start_time

def process_paramiko_stdout(process) -> tuple:
    stdout, stderr = process.communicate()
    timestamps = []
    rtts = []

    for x in stdout.decode("utf-8").split("\n"):
        components = x.split(",")
        if len(components) > 1:
            try:
                tstrip = float(components[0].strip())
                rstrip = float(components[1].strip())

                timestamps.append(tstrip)
                rtts.append(rstrip)
            except:
                pass

    print(f"[pre-processing]*=> end:{timestamps[-1]}; start:{timestamps[0]} ::==:: total: {timestamps[-1] - timestamps[0]}")
    print(f"[pre-processing]*=> timestamps length: {len(timestamps)};")

    i = 0
    for ts in timestamps:
        if start_time <= ts:
            break
        i+=1

    timestamps = timestamps[i:]
    rtts = rtts[i:]

    print(f"[post-processing]*=> end:{timestamps[-1]}; start:{timestamps[0]} ::==:: total: {timestamps[-1] - timestamps[0]}")
    print(f"[post-processing]*=> timestamps length: {len(timestamps)};")

    return timestamps, rtts

if __name__ == "__main__":

    for tick in range(20):
        for URI in URLS:
            for trace in range(TRACES):
                try:
                    print(f"[+]Trace {trace} starting: {time.time()}")
                    process = Popen(["./venv/bin/python3", "side_channel.py"], stdout=PIPE, stderr=PIPE)
                    start_time = establish_ssh_session(process.pid, URI)

                    os.system(f"kill {process.pid}")

                    time.sleep(3)

                    timestamps, rtts = process_paramiko_stdout(process)

                    df = pd.DataFrame({"timestamps": timestamps, "rtts": rtts})
                    df = {col: [df[col].tolist()] for col in df.columns}
                    df = pd.DataFrame(df)
                    df["video_id"] = pd.Series([URI])

                    print(f"[+] {df}")
                    if not os.path.exists(f"./new_data/10_per_second"):
                        os.mkdir(f"./new_data/10_per_second")

                    df.to_pickle(
                        f"./new_data/10_per_second/{URI}{time.time()}.pd",
                        compression="infer",
                        protocol=4,
                        storage_options=None,
                    )

                except Exception as ex:
                    print(ex)
