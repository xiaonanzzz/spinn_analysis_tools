import argparse
import re
import ast
import csv

class LogRetrieve():


    def __init__(self, path):
        self.path = path
        self.flags = {}
        self.info = {}
        self.retrieve_methods = [
            self.retrieve_param_numbers,
            self.retrieve_params,
            self.retrieve_best_accuracy,
        ]
        self.params_names = [
            'experiment_name', 'batch_size', 'learning_rate', 'l2_lambda', 'semantic_classifier_keep_rate',
            'embedding_keep_rate', 'learning_rate_decay_per_10k_steps', 'mlp_dim', 'model_dim', 'num_mlp_layers'
        ]

    def retrieve(self):
        with open(self.path, 'r') as txtfile:
            linei = 0
            for row in txtfile:
                linei += 1
                for f in self.retrieve_methods:
                    f(row)

    def retrieve_params(self, row):

        if self.flags.get('params', 'idle') == 'done':
            return
        elif self.flags.get('params', 'idle') == 'idle':
            if re.search('Flag values:', row) is not None:
                print 'param loading start'
                self.flags['params'] = 'start'
                self.params_txt = ''
                return  #skip this row
        elif self.flags.get('params', 'idle' == 'start'):
            self.params_txt += row
            if re.search('}\n', row) is not None:
                print 'param loading end'
                self.flags['params'] = 'done'

                # parse and clear
                params = ast.literal_eval(self.params_txt)
                for param_name in self.params_names:
                    self.info[param_name] = params[param_name]


    def retrieve_best_accuracy(self, row):
        match = re.search('Checkpointing with new best dev accuracy of (\d+\.?\d*)', row)
        if match is not None:
            self.info['best_accuracy'] = float(match.group(1))


    def retrieve_param_numbers(self, row):
        if self.flags.get('param_numbers', False) is True:
            return None

        match = re.search('Total params: (\d+)', row)
        if match is not None:
            self.info['param_numbers'] = int(match.group(1))
            self.flags['param_numbers'] = True

    def show(self):
        print self.path
        print self.info

if __name__ == '__main__':

    # # demo
    # retrieve = LogRetrieve('/Users/Alex/Repos/attspinnexplore/direct/direct-1.log')
    # retrieve.retrieve()
    # retrieve.show()

    parser = argparse.ArgumentParser('retrieve experiment info from logs')
    parser.add_argument('logs', nargs='+', help='input logs')
    parser.add_argument('--save', type=str, help='csv file to save')
    args = parser.parse_args()

    infos = []
    for log in args.logs:
        retrieve = LogRetrieve(log)
        retrieve.retrieve()
        retrieve.show()
        infos.append(retrieve.info)

    if args.save is not None and len(infos) > 0:
        with open(args.save, 'w') as csvfile:
            writer = csv.DictWriter(csvfile, infos[0].keys())
            writer.writeheader()
            writer.writerows(infos)














