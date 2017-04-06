import matplotlib.pyplot as plt
import re
import numpy as np
import argparse
import os

"""
=== examples ===
<1> plot and show but don't save:
python plot_learning_curve.py snli-spinn-1.log

<2> plot and save to file
python plot_learning_curve.py snli-spinn-1.log  --save=snli-spinn-1.png

=== The log file should follow the format ===
17-03-07 20:40:16 [1] Step: 192500 Acc: 0.84869 0.00000 Cost: 0.40663 0.25212 0.00000 0.15451 Time: 0.00214
17-03-07 21:03:56 [1] Step: 193000 Acc: 0.84769 0.00000 Cost: 0.44538 0.29133 0.00000 0.15406 Time: 0.00213
17-03-07 21:08:22 [1] Step: 193000 Eval acc: 0.853522  0.000000 ../snli_1.0/snli_1.0_dev.jsonl Time: 0.000599

*** IMPORTANT ***
The program only keep step which contains both training accuracy and evaluation accuracy
 
"""

def take_out_eval_acc(path):
    steps = []
    eval_acc = []
    with open(path) as f:
        for line in f:
            s = re.search('Step: (\d+)', line)
            if s:
                step = int(s.group(1))
                evl = re.search('Eval', line)
                if evl and (len(steps) == 0 or step > steps[-1]):
                    steps.append(step)
                    dev_acc = float(re.findall('Eval acc: (\d+\.\d+)', line)[0]) 
                    eval_acc.append(dev_acc)
                else:
                    pass
    return steps, eval_acc

parser = argparse.ArgumentParser()

parser.add_argument("log_paths", nargs='+', type=str, help="Path to log file.")
parser.add_argument("--plot_title", type=str, help="Title for plot, eg SPINN eval acc.")
parser.add_argument("--save", type=str, help="Name for saved plot.")
args = parser.parse_args()





# Pretty plot settings #
def greyGrid(ax):
    ax.spines["top"].set_visible(False)  
    ax.spines["right"].set_visible(False)
    ax.spines["bottom"].set_visible(False)  
    ax.spines["left"].set_visible(False) 
    ax.get_xaxis().tick_bottom()  
    ax.get_yaxis().tick_left() 
    ax.tick_params(axis="both", which="both", bottom="off", top="off",
               labelbottom="on", left="off", right="off", labelleft="on") 
    plt.grid(True, color='w', alpha=0.6, linestyle='-', linewidth=1.5, zorder=3)
    plt.gca().patch.set_facecolor('#f2f2f2')

plt.figure(figsize=(9,5))
ax = plt.subplot(111) 
greyGrid(ax)

for i, path in enumerate(args.log_paths):
    steps, eval_acc = take_out_eval_acc(path)
    ax.plot(steps, eval_acc, alpha=.75, zorder=4, label="{}".format(os.path.basename(path)))

# Axis and title labels
ax.set_xlabel("Step number")
ax.set_ylabel("Percentage accuracy (%)")
if args.plot_title:
    ax.set_title(args.plot_title)

# Placement of legend 
legend = ax.legend(bbox_to_anchor=(0.95, .4), prop={'size':9}, frameon = 0)
frame = legend.get_frame()
frame.set_facecolor('#f2f2f2')

plt.tight_layout()

if args.save:
    plt.savefig(args.save)
else:
	plt.show()
