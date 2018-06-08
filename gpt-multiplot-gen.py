# ---------- Configuration ----------
# Number of lines and columns (number of plots in X and Y direction)
lines = 2					
cols = 1					

# Paddings of all four sides
pad_top = 0.01
pad_bot = 0.08
pad_left = 0.06
pad_right = 0.13

# Margins between the plots
plot_x_margin = 0.008 
plot_y_margin = 0.012

# A place-holder plot-command for all plots
plot_command = "plot 1"

# Optional additional line added in front of every plot-command
plot_add = ""				

# --------- Calculate heights and widths ----------
import sys

content_height = 1.0 - pad_top - pad_bot
content_width = 1.0 - pad_left - pad_right
plot_height = (content_height - (lines - 1) * plot_y_margin) / float(lines)
plot_width = (content_width - (cols - 1) * plot_x_margin) / float(cols)

if plot_height < 0 or plot_width < 0:
    sys.stdout.write("ERROR: plot margin is too big -> negative sized plots!\n")
    sys.exit()
else:
    pass
    #sys.stdout.write("Single Plot Height: %.5f\n" % plot_height)
    #sys.stdout.write("Single Plot Width:  %.5f\n" % plot_width)

# ---------- Create margins ---------
y_margins = [[],[]]
for i in range(lines):
    tmargin = 1.0 - pad_top - i * plot_height - i * plot_y_margin
    bmargin = tmargin - plot_height
    y_margins[0].append('Y%dMARGIN' % (i + 1))
    y_margins[1].append(' = "set tmargin at screen %f; set bmargin at screen %f"' % (tmargin, bmargin))

x_margins = [[], []]
for i in range(cols):
    lmargin = (pad_left + i * plot_width + i * plot_x_margin)
    rmargin = lmargin + plot_width
    x_margins[0].append('X%dMARGIN' % (i + 1))
    x_margins[1].append(' = "set lmargin at screen %f; set rmargin at screen %f"' % (lmargin, rmargin))

# ---------- Output ----------
def compose(text):
   sys.stdout.write(text)

# 1. Definitions
# Margins
for i in range(lines):
    compose(y_margins[0][i] + y_margins[1][i] + "\n")
for i in range(cols):
    compose(x_margins[0][i] + x_margins[1][i] + "\n")
compose('\n')

# Tics
compose("NOXTICS = \"set format x ''; unset xlabel\"\n" + "NOYTICS = \"set format y ''; unset ylabel\"\n" +
        "XTICS = \"set format x '%g'; set xlabel 'X'\"\n" + "YTICS = \"set format y '%g'; set ylabel 'Y'\"\n")
compose('\n')

# 2. Multiplot command
compose("set multiplot layout %d,%d\n" % (lines, cols))
compose('\n')

# 3. Margins for each plot
for line in range(0, lines):
    for col in range(0, cols):
        this_plot = ("@%s; @%s;" % (y_margins[0][line], x_margins[0][col]))

        if line == lines - 1:
            this_plot += " @XTICS;"
        else:
            this_plot += " @NOXTICS;"

        if col == 0:
            this_plot += " @YTICS;"
        else:
            this_plot += " @NOYTICS;"

        compose(this_plot + '\n')
        if plot_add != "":
            compose(plot_add + '\n')
        compose(plot_command + '\n')
        compose('\n')

compose("unset multiplot\n")
