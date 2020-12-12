"""
Module with async executing update 1C server .bat file

Doc pages:
    - https://docs.python.org/3/library/asyncio-queue.html Async Queue
"""

import asyncio
from asyncio import Queue
import yaml
import time
from yaml import CLoader as Loader
from pprint import pprint
from random import choice
import prettytable


CMD_FILE = '.\\update_1c.bat'
HOSTS_FILE = '.\\hosts.yaml'
GLOBAL_ERROR_TABLE = prettytable.PrettyTable(('Server', 'Database name', 'Error message'))
START_TIME = time.monotonic()


def ts():
    return int(time.monotonic() - START_TIME)


def get_hosts_data(file_path):
    with open(file_path) as file:
        hosts_data = yaml.load(file, Loader=Loader)
    return hosts_data.get('hosts', {})


def generate_commands_list(hosts_data: dict):
    result_command_list = []
    for server, server_data in hosts_data.items():
        result_command_list.append(
            CMD_FILE + " " + server + " " + server_data.get('db_name')
        )
    return result_command_list


async def run_update_1c(cmd):
    proc = await asyncio.create_subprocess_shell(
        cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )

    stdout, stderr = await proc.communicate()
    await asyncio.sleep(choice([3, 4, 5, 6, 7, 8]))
    print(f'=====\n[{cmd!r} exited with {proc.returncode}] in {ts()} sec')
    if stdout:
        print(f'[stdout]\n{stdout.decode()}')
    if stderr:
        print(f'[stderr]\n{stderr.decode()}')
        
        # If Error is exists it will be added to to Global error table
        _, server_name, db_name = cmd.split()
        GLOBAL_ERROR_TABLE.add_row((
            server_name,
            db_name,
            stderr.decode()
        ))



async def worker(worker_name, queue: Queue):
    cmd = await queue.get()
    await run_update_1c(cmd)
    queue.task_done()

    print(f'Worker №{worker_name} worked {ts()} seconds with {cmd}\n=====\n')


async def main():
    commands_list = generate_commands_list(get_hosts_data(HOSTS_FILE))

    queue = asyncio.Queue()

    for cmd in commands_list:
        queue.put_nowait(cmd)

    tasks = []
    for i in range(len(commands_list)):
        task = asyncio.create_task(worker(f'{i}', queue))
        tasks.append(task)
    
    await queue.join()


if __name__ == '__main__':
    asyncio.run(main())
    print(GLOBAL_ERROR_TABLE)
