
if __name__ != "__main__": exit()

input_tsv = "labels.tsv"
ouput_file = "output.tex"
ROWS = 8
COLUMNS = 3
WIDTH_PAPER = 210
WIDTH_PRINT = 202

# XXX: Top/bottom padding for border cells should be less then center cells
CELL_PADDING_TOP = "20pt"
CELL_PADDING_BOTTOM = "34pt"
CELL_PADDING_LEFT = "1mm"

class LabelCreator:
    ii = 0
    nl = True
    begins = []

    def __init__(self, output_file, columns, rows, paper_width, print_width):
        self.fo = open(output_file, "w", encoding="utf8")
        self.columns = columns
        self.rows = rows

        # Usually printers are not able to print all the way the paper edge, so have to scale cells accordinly
        scale = print_width/paper_width
        cell_width = paper_width/columns
        self.cell_width_center = cell_width/scale
        self.cell_width_border = (paper_width - (columns-2)*self.cell_width_center)/2

        print(f"Columns: {columns}")
        print(f"Rows: {rows}")
        print(f"Paper width: {paper_width}mm")
        print(f"Print width: {print_width}mm")
        print(f"Border cell width: {self.cell_width_border}mm")
        print(f"Center cell width: {self.cell_width_center}mm")

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

    def write_cells_tabular_begin(self):
        cc = f"p{{{self.cell_width_center}mm}}"
        cb = "X"

        columns = [cb] + [cc for _ in range(self.columns - 2)] + [cb]
        self.write_begin("tabularx", "{\linewidth}{@{}" + "@{}@{}".join(columns) + "@{}}")

    def write_cell(self, line):
        self.write("\\vspace*{" + CELL_PADDING_TOP + "}")
        self.write("\\hspace*{" + CELL_PADDING_LEFT + "}")
        self.write_begin("tabular", "{l}")
        a = [s.strip() for s in line.split("\t")]
        if len(a): a[0] = self.bold(a[0])
        # XXX: Need to change the spacing manually
        self.write("\\\\".join(a))
        self.write("\\vspace*{" + CELL_PADDING_BOTTOM + "}")
        self.write_end()
        pass

    def create_labels(self, input_tsv):
        with open(input_tsv, "r", encoding="utf8") as fi, open(ouput_file, "w", encoding="utf8") as fo:
            self.write_begin("center")
            self.write("\\large")
            self.write_cells_tabular_begin()

            c = 0
            r = 0
            for line in fi.readlines():
                self.write_cell(line)
                c += 1

                if c == self.columns:
                    self.write(" \\\\", False)
                    c = 0
                    r += 1
                else:
                    self.write(" &", False)

                if c == 0 and r == self.rows:
                    self.write_end()
                    self.write("\\newpage")
                    self.write_cells_tabular_begin()
                    r = 0


            self.write_end()
            self.write_end()


LabelCreator("output.tex", COLUMNS, ROWS, WIDTH_PAPER, WIDTH_PRINT).create_labels("labels.tsv")
