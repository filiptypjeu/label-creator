
if __name__ != "__main__": exit()

input_tsv = "labels.tsv"
ouput_file = "output.tex"
rows = 8
columns = 3

class LabelCreator:
    ii = 0
    nl = True
    begins = []

    def __init__(self, output_file):
        self.fo = open(output_file, "w", encoding="utf8")

    def __del__(self):
        self.fo.close()

    @staticmethod
    def bold(str):
        return f"\\textbf{{{str}}}"

    def write_new_line(self):
        if self.nl: return
        self.nl = True
        self.fo.write("\n")

    def write(self, text, startNewLine = True):
        if startNewLine:
            self.write_new_line()
            self.fo.write(self.ii*"  ")
        self.fo.write(text)
        self.nl = False

    def indent(self, increase):
        self.ii += 1 if increase else -1
        if self.ii < 0: raise Exception("Invalid indent")

    def write_begin(self, environment, params=""):
        self.write(f"\\begin{{{environment}}}")
        self.write(params, False)
        self.indent(True)
        self.begins.append(environment)

    def write_end(self):
        self.indent(False)
        self.write(f"\\end{{{self.begins.pop()}}}")

    def write_tabular_begin(self, n, p = False):
        if p:
            env = "tabularx"
            column = f"p{{{1/n}\\linewidth}}"
            params = "{\linewidth}"
        else:
            env = "tabular"
            column = "l"
            params = ""

        self.write_begin(env, params + "{@{}" + column*n + "@{}}")

    def write_cell(self, line):
        self.write("\\hspace*{1mm}")
        self.write_tabular_begin(1)
        a = [s.strip() for s in line.split("\t")]
        if len(a): a[0] = self.bold(a[0])
        # XXX: Need to change the spacing manually
        self.write("\\\\[3mm]" + "\\\\".join(a) + "\\\\[7mm]\\phantom{a}")
        self.write_end()

    def create_labels(self, input_tsv, columns, rows):
        with open(input_tsv, "r", encoding="utf8") as fi, open(ouput_file, "w", encoding="utf8") as fo:
            self.write_begin("center")
            self.write("\\large")
            self.write_tabular_begin(columns, True)

            c = 0
            r = 0
            for line in fi.readlines():
                self.write_cell(line)
                c += 1

                if c == columns:
                    self.write(" \\\\", False)
                    c = 0
                    r += 1
                else:
                    self.write(" &", False)

                if c == 0 and r == rows:
                    self.write_end()
                    self.write("\\newpage")
                    self.write_tabular_begin(columns, True)
                    r = 0


            self.write_end()
            self.write_end()


LabelCreator("output.tex").create_labels("labels.tsv", 3, 8)
