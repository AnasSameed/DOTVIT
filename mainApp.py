from flask import Flask, render_template, request
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns  # Import Seaborn for additional plots
import io
import base64
# from Bio import Phylo
# from io import StringIO
# from Bio import Phylo
# from Bio.Phylo.TreeConstruction import DistanceTreeConstructor, DistanceCalculator
# from Bio.Align import MultipleSeqAlignment
# from Bio.Seq import Seq
# from Bio.SeqRecord import SeqRecord

file = ''
app = Flask(__name__, template_folder=file)

def generate_dot(seq1, seq2):
    len_seq1 = len(seq1)
    len_seq2 = len(seq2)
    dotmatrix = np.zeros((len_seq1, len_seq2))

    for i in range(len_seq1):
        for j in range(len_seq2):
            if seq1[i] == seq2[j]:
                dotmatrix[i][j] = 1

    plt.imshow(dotmatrix, cmap='Greys', interpolation='none', aspect='auto')
    plt.title('Dot Plot')
    plt.ylabel('Sequence 2')
    plt.xlabel('Sequence 1')
    plt.xticks(range(len_seq2), list(seq2))
    plt.yticks(range(len_seq1), list(seq1))

    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    img_base64 = base64.b64encode(img.getvalue()).decode()
    plt.close()

    return img_base64

def generate_histogram(seq1, seq2):
    combined_seq = seq1 + seq2
    characters = sorted(set(combined_seq))
    counts = [combined_seq.count(char) for char in characters]

    plt.bar(characters, counts, color='blue')
    plt.title('Character Frequency Histogram')
    plt.xlabel('Characters')
    plt.ylabel('Frequency')

    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    img_base64 = base64.b64encode(img.getvalue()).decode()
    plt.close()

    return img_base64

def generate_gc_content_plot(seq1, seq2):
    def gc_content(seq):
        return (seq.count('G') + seq.count('C')) / len(seq) * 100

    gc_contents = [gc_content(seq1), gc_content(seq2)]
    labels = ['Sequence 1', 'Sequence 2']

    plt.bar(labels, gc_contents, color='green')
    plt.title('GC Content')
    plt.ylabel('GC Content (%)')

    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    img_base64 = base64.b64encode(img.getvalue()).decode()
    plt.close()

    return img_base64

def generate_violin_plot(seq1, seq2):
    # Example data for violin plot (replace with your own)
    data = np.random.randn(100, 2)

    violin = sns.violinplot(data=data)
    plt.title('Violin Plot')

    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    img_base64 = base64.b64encode(img.getvalue()).decode()
    plt.close()

    return img_base64


def generate_heatmap(seq1, seq2):
    # Example data for heatmap (replace with your own)
    data = np.random.rand(10, 10)

    heatmap = sns.heatmap(data)
    plt.title('Heatmap')

    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    img_base64 = base64.b64encode(img.getvalue()).decode()
    plt.close()

    return img_base64
# def generate_scatter_plot(seq1, seq2):
#     positions = list(range(len(seq1)))
#     values1 = [ord(char) for char in seq1]
#     values2 = [ord(char) for char in seq2]
#
#     plt.scatter(positions, values1, alpha=0.5, label='Sequence 1')
#     plt.scatter(positions, values2, alpha=0.5, label='Sequence 2')
#     plt.xlabel('Position')
#     plt.ylabel('Value')
#     plt.title('Scatter Plot of Sequences')
#     plt.legend()
#
#     img = io.BytesIO()
#     plt.savefig(img, format='png')
#     img.seek(0)
#     img_base64 = base64.b64encode(img.getvalue()).decode()
#     plt.close()
#
#     return img_base64

def generate_scatter_plot(seq1, seq2):
    length = max(len(seq1), len(seq2))
    positions = list(range(length))

    values1 = [ord(char) for char in seq1] + [None] * (length - len(seq1))
    values2 = [ord(char) for char in seq2] + [None] * (length - len(seq2))

    paired_positions = [i for i in range(length) if i < len(seq1) and i < len(seq2)]
    unpaired_positions_seq1 = [i for i in range(len(seq1), length)]
    unpaired_positions_seq2 = [i for i in range(len(seq2), length)]

    plt.scatter(paired_positions, [values1[i] for i in paired_positions], alpha=0.5, label='Sequence 1 (Paired)')
    plt.scatter(paired_positions, [values2[i] for i in paired_positions], alpha=0.5, label='Sequence 2 (Paired)')

    plt.scatter(unpaired_positions_seq1, [values1[i] for i in unpaired_positions_seq1], alpha=0.5,
                label='Sequence 1 (Unpaired)')
    plt.scatter(unpaired_positions_seq2, [values2[i] for i in unpaired_positions_seq2], alpha=0.5,
                label='Sequence 2 (Unpaired)')

    plt.xlabel('Position')
    plt.ylabel('Value')
    plt.title('Scatter Plot of Sequences')

    # Update the y-axis with sequence names
    plt.yticks([ord('A'), ord('C'), ord('G'), ord('T')], ['A', 'C', 'G', 'T'])

    plt.legend()

    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    img_base64 = base64.b64encode(img.getvalue()).decode()
    plt.close()

    return img_base64


# def generate_multiple_sequence_plot(seq1, seq2):
#     sequences = [seq1, seq2]
#     fig, axes = plt.subplots(1, len(sequences), figsize=(len(sequences) * 5, 5), subplot_kw={'projection': 'polar'})
#
#     for ax, seq in zip(axes, sequences):
#         length = len(seq)
#         positions = list(range(length))
#
#         values = [ord(char) for char in seq]
#
#         theta = [2 * np.pi * (i / length) for i in positions]
#         radii = values
#
#         ax.scatter(theta, radii, alpha=0.5)
#         ax.set_yticks([ord('A'), ord('C'), ord('G'), ord('T')])
#         ax.set_yticklabels(['A', 'C', 'G', 'T'])
#         ax.set_xticks([])
#         ax.set_title(f'Sequence: {seq}')
#
#     fig.tight_layout()
#
#     img = io.BytesIO()
#     plt.savefig(img, format='png')
#     img.seek(0)
#     img_base64 = base64.b64encode(img.getvalue()).decode()
#     plt.close()
#
#     return img_base64
def generate_multiple_sequence_plot(seq1, seq2):
    sequences = [seq1, seq2]
    colors = ['blue', 'green']

    fig, axes = plt.subplots(1, len(sequences), figsize=(len(sequences) * 5, 5), subplot_kw={'projection': 'polar'})

    for ax, seq, color in zip(axes, sequences, colors):
        length = len(seq)
        positions = list(range(length))

        values = [ord(char) for char in seq]

        theta = [2 * np.pi * (i / length) for i in positions]
        radii = values

        ax.scatter(theta, radii, alpha=0.5, color=color, label=f'Sequence: {seq}')
        ax.set_yticks([ord('A'), ord('C'), ord('G'), ord('T')])
        ax.set_yticklabels(['A', 'C', 'G', 'T'])
        ax.set_xticks([])
        ax.set_ylim(50, 75)  # Adding a gap in the chart by adjusting the limits
        ax.legend()
        ax.set_title(f'Sequence: {seq}')

    fig.tight_layout()

    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    img_base64 = base64.b64encode(img.getvalue()).decode()
    plt.close()

    return img_base64


def generate_phylogenetic_tree(seq1, seq2):
    records = [SeqRecord(Seq(seq1), id="Seq1"), SeqRecord(Seq(seq2), id="Seq2")]
    alignment = MultipleSeqAlignment(records)
    calculator = DistanceCalculator('identity')
    constructor = DistanceTreeConstructor(calculator, 'nj')
    tree = constructor.build_tree(alignment)

    img = io.BytesIO()
    Phylo.draw(tree, do_show=False)
    plt.savefig(img, format='png')
    img.seek(0)
    img_base64 = base64.b64encode(img.getvalue()).decode()
    plt.close()

    return img_base64
@app.route('/', methods=['GET', 'POST'])
def index():
    dot_plot = histogram = gc_content_plot = scatter_plot= multiple= tree = None
    selected_graphs = []
    if request.method == 'POST':
        sequence1 = request.form['sequence1']
        sequence2 = request.form['sequence2']

        selected_graphs = request.form.getlist('graphs')

        if 'dot_plot' in selected_graphs:
            dot_plot = generate_dot(sequence1, sequence2)
        if 'histogram' in selected_graphs:
            histogram = generate_histogram(sequence1, sequence2)
        if 'gc_content_plot' in selected_graphs:
            gc_content_plot = generate_gc_content_plot(sequence1, sequence2)
        if 'multiple' in selected_graphs:
            multiple = generate_multiple_sequence_plot(sequence1, sequence2)

        if 'scatter_plot' in selected_graphs:
            scatter_plot = generate_scatter_plot(sequence1, sequence2)
        if 'tree' in selected_graphs:
            tree = generate_phylogenetic_tree(sequence1, sequence2)


    return render_template('index.html', dot_plot=dot_plot, histogram=histogram, gc_content_plot=gc_content_plot,
scatter_plot=scatter_plot,multiple=multiple,tree = tree,selected_graphs=selected_graphs)


if __name__ == '__main__':
    app.run(host="0.0.0.0",debug=True, port=5500)
