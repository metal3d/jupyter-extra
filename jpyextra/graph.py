import tensorflow as tf
import numpy as np
from IPython.display import display, HTML


DEFAULT_GRAPH_WIDTH = 800
DEFAULT_GRAPH_HEIGHT = 600


def strip_consts(graph_def, max_const_size=32):
    """Strip large constant values from graph_def."""
    strip_def = tf.GraphDef()
    for n0 in graph_def.node:
        n = strip_def.node.add()
        n.MergeFrom(n0)
        if n.op == 'Const':
            tensor = n.attr['value'].tensor
            size = len(tensor.tensor_content)
            if size > max_const_size:
                tensor.tensor_content = tf.compat.as_bytes(
                        "<stripped %d bytes>" % size)
    return strip_def


def rename_nodes(graph_def, rename_func):
    """ Rename nodes in graph

    Parameters:
    - graph_def: tf.graph_def
    - rename_func: function to rename on node (fn(nodename) -> new name)

    Returns:
    - resulting graph def

    Taken and adapted from:
    https://github.com/tensorflow/tensorflow/blob/master/tensorflow/examples/tutorials/deepdream/deepdream.ipynb<Paste>
    """
    res_def = tf.GraphDef()
    for n0 in graph_def.node:
        n = res_def.node.add()
        n.MergeFrom(n0)
        n.name = rename_func(n.name)
        for i, s in enumerate(n.input):
            n.input[i] = rename_func(s) \
                if s[0] != '^' else '^'+rename_func(s[1:])
    return res_def


def show_graph(
        graph_def,
        max_const_size=32,
        width=DEFAULT_GRAPH_WIDTH,
        height=DEFAULT_GRAPH_HEIGHT):
    """Visualize TensorFlow graph.

    It displays a interactive graph visualisation on Jupyter Notebooks.

    Parameters:
    - graph_def: tensorflow.graph or graphdef to visualize
    - width and height: sizes in pixel for the view
    - max_const_size: size max for constant

    Taken and adapted from:
    https://github.com/tensorflow/tensorflow/blob/master/tensorflow/examples/tutorials/deepdream/deepdream.ipynb<Paste>
    """
    if hasattr(graph_def, 'as_graph_def'):
        graph_def = graph_def.as_graph_def()
    strip_def = strip_consts(graph_def, max_const_size=max_const_size)
    graphurl = 'https://tensorboard.appspot.com/tf-graph-basic.build.html'
    code = """
        <script>
          function load() {{
            document.getElementById("{id}").pbtxt = {data};
          }}
        </script>
        <link rel="import" href="{graphurl}" onload=load()>
        <div style="height:{height}px">
          <tf-graph-basic id="{id}"></tf-graph-basic>
        </div>
    """.format(
            data=repr(str(strip_def)),
            id='graph'+str(np.random.rand()),
            height=str(height),
            graphurl=graphurl)

    iframe = """
        <iframe seamless
        style="width:{width}px;height:{height}px;border:0" srcdoc="{code}">
        </iframe>
    """.format(
            code=code.replace('"', '&quot;'),
            width=width,
            height=str(height + 20),
        )

    display(HTML(iframe))
