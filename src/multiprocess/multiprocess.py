import os
import multiprocessing as mp
from functools import partial

def mp_proxy(iterable, func,static_func_kwargs={}, map_type="imap", context="fork", processes=-1, chunksize=1):
    if processes == -1:
        processes = int(len(os.sched_getaffinity(0))/2)
    print(f"spawning {processes} processes")

    with mp.get_context(context).Pool(processes=processes) as pool:
        if map_type == "imap":
            map_func = pool.imap
        elif map_type == "imap_unordered":
            map_func = pool.imap_unordered
        res = map_func(partial(func,  **static_func_kwargs), iterable, chunksize=chunksize)
        for res_i in res:
            yield res_i