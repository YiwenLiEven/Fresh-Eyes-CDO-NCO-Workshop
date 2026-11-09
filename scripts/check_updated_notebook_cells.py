"""Execute notebook cells with IPython in-process when a kernel socket is unavailable.

This verifies the prepared cell code, including direct CDO/NCO commands, but is NOT a live Jupyter
or Binder test. Normal Binder builds should still use nbconvert --execute.
"""
from pathlib import Path
import argparse
import json
import os
import sys
import time
import nbformat
from IPython.core.interactiveshell import InteractiveShell
from IPython.utils.capture import capture_output


def main():
    p=argparse.ArgumentParser();p.add_argument('notebook');p.add_argument('--receipt',required=True)
    args=p.parse_args()
    notebook=Path(args.notebook).resolve();receipt=Path(args.receipt).resolve()
    root=Path(__file__).resolve().parents[1];os.chdir(root)
    nb=nbformat.read(notebook,as_version=4);nbformat.validate(nb)
    shell=InteractiveShell.instance()
    result={'notebook':str(notebook.relative_to(root)),
            'execution_method':'IPython in-process; no Jupyter kernel, browser or Binder session',
            'live_jupyter_verified':False,'cells':[],'passed':False}
    start=time.time()
    for index,cell in enumerate(nb.cells):
        if cell.cell_type!='code':continue
        print(f'Executing code cell {index+1}',flush=True)
        with capture_output() as captured:
            run=shell.run_cell(cell.source,store_history=False)
        entry={'cell_number':index+1,'passed':not bool(run.error_before_exec or run.error_in_exec),
               'stdout':captured.stdout,'stderr':captured.stderr}
        result['cells'].append(entry)
        if not entry['passed']:
            result['error']=str(run.error_before_exec or run.error_in_exec)
            break
    else: result['passed']=True
    result['elapsed_seconds']=time.time()-start
    if 'RUN' in shell.user_ns: result['output_root']=str(shell.user_ns['RUN'].relative_to(root))
    receipt.parent.mkdir(parents=True,exist_ok=True)
    receipt.write_text(json.dumps(result,indent=2)+'\n')
    print(('PASS' if result['passed'] else 'FAIL')+': '+str(receipt))
    if not result['passed']: raise SystemExit(1)

if __name__=='__main__':main()
