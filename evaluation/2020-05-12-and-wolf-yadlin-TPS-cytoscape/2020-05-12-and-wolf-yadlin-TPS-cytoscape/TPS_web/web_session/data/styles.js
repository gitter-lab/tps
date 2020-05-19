var styles = [ {
  "format_version" : "1.0",
  "generated_by" : "cytoscape-3.7.1",
  "target_cytoscapejs_version" : "~2.1",
  "title" : "Big Labels",
  "style" : [ {
    "selector" : "node",
    "css" : {
      "border-width" : 0.0,
      "height" : 5.0,
      "color" : "rgb(51,51,51)",
      "text-opacity" : 1.0,
      "text-valign" : "center",
      "text-halign" : "center",
      "background-color" : "rgb(255,255,255)",
      "border-color" : "rgb(0,0,0)",
      "border-opacity" : 1.0,
      "font-size" : 24,
      "font-family" : "SansSerif.plain",
      "font-weight" : "normal",
      "shape" : "ellipse",
      "width" : 5.0,
      "background-opacity" : 1.0,
      "content" : "data(name)"
    }
  }, {
    "selector" : "node:selected",
    "css" : {
      "background-color" : "rgb(255,0,102)"
    }
  }, {
    "selector" : "edge",
    "css" : {
      "target-arrow-color" : "rgb(0,0,0)",
      "source-arrow-color" : "rgb(0,0,0)",
      "font-family" : "SansSerif.plain",
      "font-weight" : "normal",
      "line-color" : "rgb(183,183,183)",
      "color" : "rgb(0,0,0)",
      "target-arrow-shape" : "none",
      "source-arrow-shape" : "none",
      "line-style" : "solid",
      "font-size" : 10,
      "text-opacity" : 1.0,
      "content" : "",
      "width" : 1.0,
      "opacity" : 1.0
    }
  }, {
    "selector" : "edge:selected",
    "css" : {
      "line-color" : "rgb(255,0,0)"
    }
  } ]
}, {
  "format_version" : "1.0",
  "generated_by" : "cytoscape-3.7.1",
  "target_cytoscapejs_version" : "~2.1",
  "title" : "Nested Network Style",
  "style" : [ {
    "selector" : "node",
    "css" : {
      "border-width" : 2.0,
      "height" : 40.0,
      "color" : "rgb(0,0,0)",
      "text-opacity" : 1.0,
      "text-valign" : "center",
      "text-halign" : "center",
      "background-color" : "rgb(255,255,255)",
      "border-color" : "rgb(0,0,0)",
      "border-opacity" : 1.0,
      "font-size" : 12,
      "font-family" : "SansSerif.plain",
      "font-weight" : "normal",
      "shape" : "ellipse",
      "width" : 60.0,
      "background-opacity" : 1.0,
      "content" : "data(shared_name)"
    }
  }, {
    "selector" : "node[has_nested_network]",
    "css" : {
      "background-color" : "rgb(255,255,255)"
    }
  }, {
    "selector" : "node[has_nested_network]",
    "css" : {
      "shape" : "rectangle"
    }
  }, {
    "selector" : "node[has_nested_network]",
    "css" : {
      "color" : "rgb(0,102,204)"
    }
  }, {
    "selector" : "node[has_nested_network]",
    "css" : {
      "border-color" : "rgb(0,102,204)"
    }
  }, {
    "selector" : "node[has_nested_network]",
    "css" : {
      "text-valign" : "bottom"
    }
  }, {
    "selector" : "node:selected",
    "css" : {
      "background-color" : "rgb(255,255,0)"
    }
  }, {
    "selector" : "edge",
    "css" : {
      "target-arrow-color" : "rgb(0,0,0)",
      "source-arrow-color" : "rgb(0,0,0)",
      "font-family" : "SansSerif.plain",
      "font-weight" : "normal",
      "line-color" : "rgb(64,64,64)",
      "color" : "rgb(0,0,0)",
      "target-arrow-shape" : "none",
      "source-arrow-shape" : "none",
      "line-style" : "solid",
      "font-size" : 10,
      "text-opacity" : 1.0,
      "content" : "",
      "width" : 1.0,
      "opacity" : 1.0
    }
  }, {
    "selector" : "edge:selected",
    "css" : {
      "line-color" : "rgb(255,0,0)"
    }
  } ]
}, {
  "format_version" : "1.0",
  "generated_by" : "cytoscape-3.7.1",
  "target_cytoscapejs_version" : "~2.1",
  "title" : "Marquee",
  "style" : [ {
    "selector" : "node",
    "css" : {
      "border-width" : 10.0,
      "height" : 20.0,
      "color" : "rgb(102,102,102)",
      "text-opacity" : 1.0,
      "text-valign" : "bottom",
      "text-halign" : "center",
      "background-color" : "rgb(0,204,255)",
      "border-color" : "rgb(255,255,255)",
      "border-opacity" : 1.0,
      "font-size" : 12,
      "font-family" : "SansSerif.plain",
      "font-weight" : "normal",
      "shape" : "ellipse",
      "width" : 20.0,
      "background-opacity" : 1.0,
      "content" : "data(name)"
    }
  }, {
    "selector" : "node:selected",
    "css" : {
      "background-color" : "rgb(255,0,102)"
    }
  }, {
    "selector" : "edge",
    "css" : {
      "target-arrow-color" : "rgb(255,255,255)",
      "source-arrow-color" : "rgb(255,255,255)",
      "font-family" : "SansSerif.plain",
      "font-weight" : "normal",
      "line-color" : "rgb(255,255,255)",
      "color" : "rgb(102,102,102)",
      "target-arrow-shape" : "triangle",
      "source-arrow-shape" : "none",
      "line-style" : "dashed",
      "font-size" : 8,
      "text-opacity" : 1.0,
      "width" : 2.0,
      "opacity" : 1.0,
      "content" : "data(interaction)"
    }
  }, {
    "selector" : "edge:selected",
    "css" : {
      "line-color" : "rgb(255,0,0)"
    }
  } ]
}, {
  "format_version" : "1.0",
  "generated_by" : "cytoscape-3.7.1",
  "target_cytoscapejs_version" : "~2.1",
  "title" : "Minimal",
  "style" : [ {
    "selector" : "node",
    "css" : {
      "border-width" : 0.0,
      "height" : 42.0,
      "color" : "rgb(51,51,51)",
      "text-opacity" : 1.0,
      "text-valign" : "center",
      "text-halign" : "center",
      "background-color" : "rgb(255,255,255)",
      "border-color" : "rgb(0,0,0)",
      "border-opacity" : 1.0,
      "font-size" : 9,
      "font-family" : "SansSerif.plain",
      "font-weight" : "normal",
      "shape" : "rectangle",
      "width" : 42.0,
      "background-opacity" : 1.0,
      "content" : "data(name)"
    }
  }, {
    "selector" : "node:selected",
    "css" : {
      "background-color" : "rgb(255,255,0)"
    }
  }, {
    "selector" : "edge",
    "css" : {
      "target-arrow-color" : "rgb(0,0,0)",
      "source-arrow-color" : "rgb(0,0,0)",
      "font-family" : "SansSerif.plain",
      "font-weight" : "normal",
      "line-color" : "rgb(76,76,76)",
      "color" : "rgb(0,0,0)",
      "target-arrow-shape" : "none",
      "source-arrow-shape" : "none",
      "line-style" : "solid",
      "font-size" : 10,
      "text-opacity" : 1.0,
      "content" : "",
      "width" : 2.0,
      "opacity" : 1.0
    }
  }, {
    "selector" : "edge:selected",
    "css" : {
      "line-color" : "rgb(255,0,0)"
    }
  } ]
}, {
  "format_version" : "1.0",
  "generated_by" : "cytoscape-3.7.1",
  "target_cytoscapejs_version" : "~2.1",
  "title" : "default",
  "style" : [ {
    "selector" : "node",
    "css" : {
      "border-width" : 0.0,
      "height" : 35.0,
      "color" : "rgb(0,0,0)",
      "text-opacity" : 1.0,
      "text-valign" : "center",
      "text-halign" : "center",
      "background-color" : "rgb(137,208,245)",
      "border-color" : "rgb(204,204,204)",
      "border-opacity" : 1.0,
      "font-size" : 12,
      "font-family" : "SansSerif.plain",
      "font-weight" : "normal",
      "shape" : "roundrectangle",
      "width" : 75.0,
      "background-opacity" : 1.0,
      "content" : "data(name)"
    }
  }, {
    "selector" : "node:selected",
    "css" : {
      "background-color" : "rgb(255,255,0)"
    }
  }, {
    "selector" : "edge",
    "css" : {
      "target-arrow-color" : "rgb(0,0,0)",
      "source-arrow-color" : "rgb(0,0,0)",
      "font-family" : "Dialog.plain",
      "font-weight" : "normal",
      "line-color" : "rgb(132,132,132)",
      "color" : "rgb(0,0,0)",
      "target-arrow-shape" : "none",
      "source-arrow-shape" : "none",
      "line-style" : "solid",
      "font-size" : 10,
      "text-opacity" : 1.0,
      "content" : "",
      "width" : 2.0,
      "opacity" : 1.0
    }
  }, {
    "selector" : "edge:selected",
    "css" : {
      "line-color" : "rgb(255,0,0)"
    }
  } ]
}, {
  "format_version" : "1.0",
  "generated_by" : "cytoscape-3.7.1",
  "target_cytoscapejs_version" : "~2.1",
  "title" : "Ripple",
  "style" : [ {
    "selector" : "node",
    "css" : {
      "border-width" : 20.0,
      "height" : 50.0,
      "color" : "rgb(19,58,96)",
      "text-opacity" : 1.0,
      "text-valign" : "center",
      "text-halign" : "center",
      "background-color" : "rgb(255,255,255)",
      "border-color" : "rgb(51,153,255)",
      "border-opacity" : 1.0,
      "font-size" : 8,
      "font-family" : "SansSerif.plain",
      "font-weight" : "normal",
      "shape" : "ellipse",
      "width" : 50.0,
      "background-opacity" : 1.0,
      "content" : "data(name)"
    }
  }, {
    "selector" : "node:selected",
    "css" : {
      "background-color" : "rgb(255,255,204)"
    }
  }, {
    "selector" : "edge",
    "css" : {
      "target-arrow-color" : "rgb(0,0,0)",
      "source-arrow-color" : "rgb(0,0,0)",
      "font-family" : "SansSerif.plain",
      "font-weight" : "normal",
      "line-color" : "rgb(51,153,255)",
      "color" : "rgb(0,0,0)",
      "target-arrow-shape" : "none",
      "source-arrow-shape" : "none",
      "line-style" : "solid",
      "font-size" : 10,
      "text-opacity" : 1.0,
      "content" : "",
      "width" : 3.0,
      "opacity" : 1.0
    }
  }, {
    "selector" : "edge:selected",
    "css" : {
      "line-color" : "rgb(255,0,0)"
    }
  } ]
}, {
  "format_version" : "1.0",
  "generated_by" : "cytoscape-3.7.1",
  "target_cytoscapejs_version" : "~2.1",
  "title" : "Sample1",
  "style" : [ {
    "selector" : "node",
    "css" : {
      "border-width" : 0.0,
      "height" : 25.0,
      "color" : "rgb(51,51,51)",
      "text-opacity" : 1.0,
      "text-valign" : "center",
      "text-halign" : "center",
      "background-color" : "rgb(127,205,187)",
      "border-color" : "rgb(0,0,0)",
      "border-opacity" : 1.0,
      "font-size" : 10,
      "font-family" : "Dialog.plain",
      "font-weight" : "normal",
      "shape" : "ellipse",
      "width" : 25.0,
      "background-opacity" : 1.0,
      "content" : "data(name)"
    }
  }, {
    "selector" : "node:selected",
    "css" : {
      "background-color" : "rgb(255,255,0)"
    }
  }, {
    "selector" : "edge",
    "css" : {
      "target-arrow-color" : "rgb(0,0,0)",
      "source-arrow-color" : "rgb(0,0,0)",
      "font-family" : "Dialog.plain",
      "font-weight" : "normal",
      "line-color" : "rgb(153,153,153)",
      "color" : "rgb(51,51,51)",
      "target-arrow-shape" : "none",
      "source-arrow-shape" : "none",
      "line-style" : "solid",
      "font-size" : 10,
      "text-opacity" : 1.0,
      "width" : 1.0,
      "opacity" : 1.0,
      "content" : "data(interaction)"
    }
  }, {
    "selector" : "edge[interaction = 'pp']",
    "css" : {
      "line-style" : "solid"
    }
  }, {
    "selector" : "edge[interaction = 'pd']",
    "css" : {
      "line-style" : "dashed"
    }
  }, {
    "selector" : "edge:selected",
    "css" : {
      "line-color" : "rgb(255,0,0)"
    }
  } ]
}, {
  "format_version" : "1.0",
  "generated_by" : "cytoscape-3.7.1",
  "target_cytoscapejs_version" : "~2.1",
  "title" : "Directed",
  "style" : [ {
    "selector" : "node",
    "css" : {
      "border-width" : 5.0,
      "height" : 45.0,
      "color" : "rgb(51,153,255)",
      "text-opacity" : 1.0,
      "text-valign" : "center",
      "text-halign" : "center",
      "background-color" : "rgb(255,255,255)",
      "border-color" : "rgb(145,145,145)",
      "border-opacity" : 1.0,
      "font-size" : 8,
      "font-family" : "SansSerif.plain",
      "font-weight" : "normal",
      "shape" : "ellipse",
      "width" : 45.0,
      "background-opacity" : 1.0,
      "content" : "data(name)"
    }
  }, {
    "selector" : "node:selected",
    "css" : {
      "background-color" : "rgb(255,0,102)"
    }
  }, {
    "selector" : "edge",
    "css" : {
      "target-arrow-color" : "rgb(204,204,204)",
      "source-arrow-color" : "rgb(204,204,204)",
      "font-family" : "SansSerif.plain",
      "font-weight" : "normal",
      "line-color" : "rgb(204,204,204)",
      "color" : "rgb(51,153,255)",
      "target-arrow-shape" : "triangle",
      "source-arrow-shape" : "none",
      "line-style" : "solid",
      "font-size" : 12,
      "text-opacity" : 1.0,
      "width" : 5.0,
      "opacity" : 1.0,
      "content" : "data(interaction)"
    }
  }, {
    "selector" : "edge:selected",
    "css" : {
      "line-color" : "rgb(255,0,0)"
    }
  } ]
}, {
  "format_version" : "1.0",
  "generated_by" : "cytoscape-3.7.1",
  "target_cytoscapejs_version" : "~2.1",
  "title" : "Sample2",
  "style" : [ {
    "selector" : "node",
    "css" : {
      "border-width" : 15.0,
      "height" : 50.0,
      "color" : "rgb(102,102,102)",
      "text-opacity" : 1.0,
      "text-valign" : "center",
      "text-halign" : "right",
      "background-color" : "rgb(58,127,182)",
      "border-color" : "rgb(255,255,255)",
      "border-opacity" : 1.0,
      "font-size" : 20,
      "font-family" : "Dialog.plain",
      "font-weight" : "normal",
      "shape" : "ellipse",
      "width" : 50.0,
      "background-opacity" : 1.0,
      "content" : "data(name)"
    }
  }, {
    "selector" : "node:selected",
    "css" : {
      "background-color" : "rgb(255,255,0)"
    }
  }, {
    "selector" : "edge",
    "css" : {
      "target-arrow-color" : "rgb(0,0,0)",
      "source-arrow-color" : "rgb(0,0,0)",
      "font-family" : "SansSerif.plain",
      "font-weight" : "normal",
      "line-color" : "rgb(255,255,255)",
      "color" : "rgb(0,0,0)",
      "target-arrow-shape" : "none",
      "source-arrow-shape" : "none",
      "line-style" : "solid",
      "font-size" : 10,
      "text-opacity" : 1.0,
      "content" : "",
      "width" : 20.0,
      "opacity" : 1.0
    }
  }, {
    "selector" : "edge:selected",
    "css" : {
      "line-color" : "rgb(255,0,0)"
    }
  } ]
}, {
  "format_version" : "1.0",
  "generated_by" : "cytoscape-3.7.1",
  "target_cytoscapejs_version" : "~2.1",
  "title" : "TPS",
  "style" : [ {
    "selector" : "node",
    "css" : {
      "border-width" : 1.0,
      "height" : 40.0,
      "color" : "rgb(0,0,0)",
      "text-opacity" : 1.0,
      "text-valign" : "top",
      "text-halign" : "center",
      "background-color" : "rgb(255,255,255)",
      "border-color" : "rgb(0,0,0)",
      "border-opacity" : 1.0,
      "font-size" : 12,
      "font-family" : "Dialog.plain",
      "font-weight" : "normal",
      "shape" : "roundrectangle",
      "width" : 45.0,
      "background-opacity" : 1.0,
      "content" : "data(Gene)"
    }
  }, {
    "selector" : "node[ReferencePathway]",
    "css" : {
      "shape" : "roundrectangle"
    }
  }, {
    "selector" : "node[!ReferencePathway]",
    "css" : {
      "shape" : "rectangle"
    }
  }, {
    "selector" : "node[ReferencePathway]",
    "css" : {
      "border-width" : 6.0
    }
  }, {
    "selector" : "node[!ReferencePathway]",
    "css" : {
      "border-width" : 1.0
    }
  }, {
    "selector" : "node:selected",
    "css" : {
      "background-color" : "rgb(255,255,0)"
    }
  }, {
    "selector" : "edge",
    "css" : {
      "target-arrow-color" : "rgb(64,64,64)",
      "source-arrow-color" : "rgb(64,64,64)",
      "font-family" : "Dialog.plain",
      "font-weight" : "normal",
      "line-color" : "rgb(64,64,64)",
      "color" : "rgb(0,0,0)",
      "target-arrow-shape" : "none",
      "source-arrow-shape" : "none",
      "line-style" : "solid",
      "font-size" : 10,
      "text-opacity" : 1.0,
      "content" : "",
      "width" : 1.0,
      "opacity" : 0.7843137254901961
    }
  }, {
    "selector" : "edge[interaction = 'A']",
    "css" : {
      "target-arrow-shape" : "triangle"
    }
  }, {
    "selector" : "edge[interaction = 'U']",
    "css" : {
      "target-arrow-shape" : "none"
    }
  }, {
    "selector" : "edge[interaction = 'I']",
    "css" : {
      "target-arrow-shape" : "tee"
    }
  }, {
    "selector" : "edge[interaction = 'N']",
    "css" : {
      "target-arrow-shape" : "circle"
    }
  }, {
    "selector" : "edge[interaction = 'A']",
    "css" : {
      "line-color" : "rgb(0,155,0)",
      "target-arrow-color" : "rgb(0,155,0)",
      "source-arrow-color" : "rgb(0,155,0)"
    }
  }, {
    "selector" : "edge[interaction = 'U']",
    "css" : {
      "line-color" : "rgb(102,102,102)",
      "target-arrow-color" : "rgb(102,102,102)",
      "source-arrow-color" : "rgb(102,102,102)"
    }
  }, {
    "selector" : "edge[interaction = 'I']",
    "css" : {
      "line-color" : "rgb(217,42,42)",
      "target-arrow-color" : "rgb(217,42,42)",
      "source-arrow-color" : "rgb(217,42,42)"
    }
  }, {
    "selector" : "edge[interaction = 'N']",
    "css" : {
      "line-color" : "rgb(102,102,102)",
      "target-arrow-color" : "rgb(102,102,102)",
      "source-arrow-color" : "rgb(102,102,102)"
    }
  }, {
    "selector" : "edge[interaction = 'A']",
    "css" : {
      "width" : 4.0
    }
  }, {
    "selector" : "edge[interaction = 'U']",
    "css" : {
      "width" : 1.0
    }
  }, {
    "selector" : "edge[interaction = 'I']",
    "css" : {
      "width" : 4.0
    }
  }, {
    "selector" : "edge[interaction = 'N']",
    "css" : {
      "width" : 4.0
    }
  }, {
    "selector" : "edge:selected",
    "css" : {
      "line-color" : "rgb(255,0,0)"
    }
  } ]
}, {
  "format_version" : "1.0",
  "generated_by" : "cytoscape-3.7.1",
  "target_cytoscapejs_version" : "~2.1",
  "title" : "Curved",
  "style" : [ {
    "selector" : "node",
    "css" : {
      "border-width" : 7.0,
      "height" : 18.0,
      "color" : "rgb(102,102,102)",
      "text-opacity" : 1.0,
      "text-valign" : "bottom",
      "text-halign" : "right",
      "background-color" : "rgb(254,196,79)",
      "border-color" : "rgb(255,255,255)",
      "border-opacity" : 1.0,
      "font-size" : 14,
      "font-family" : "SansSerif.plain",
      "font-weight" : "normal",
      "shape" : "ellipse",
      "width" : 18.0,
      "background-opacity" : 1.0,
      "content" : "data(name)"
    }
  }, {
    "selector" : "node:selected",
    "css" : {
      "background-color" : "rgb(255,255,0)"
    }
  }, {
    "selector" : "edge",
    "css" : {
      "target-arrow-color" : "rgb(255,255,255)",
      "source-arrow-color" : "rgb(255,255,255)",
      "font-family" : "SansSerif.plain",
      "font-weight" : "normal",
      "line-color" : "rgb(255,255,255)",
      "color" : "rgb(0,0,0)",
      "target-arrow-shape" : "triangle",
      "source-arrow-shape" : "none",
      "line-style" : "solid",
      "font-size" : 10,
      "text-opacity" : 1.0,
      "content" : "",
      "width" : 3.0,
      "opacity" : 1.0
    }
  }, {
    "selector" : "edge:selected",
    "css" : {
      "line-color" : "rgb(255,0,0)"
    }
  } ]
}, {
  "format_version" : "1.0",
  "generated_by" : "cytoscape-3.7.1",
  "target_cytoscapejs_version" : "~2.1",
  "title" : "default black",
  "style" : [ {
    "selector" : "node",
    "css" : {
      "border-width" : 0.0,
      "height" : 15.0,
      "color" : "rgb(204,204,204)",
      "text-opacity" : 1.0,
      "text-valign" : "bottom",
      "text-halign" : "right",
      "background-color" : "rgb(255,255,255)",
      "border-color" : "rgb(0,153,0)",
      "border-opacity" : 1.0,
      "font-size" : 12,
      "font-family" : "SansSerif.plain",
      "font-weight" : "normal",
      "shape" : "ellipse",
      "width" : 15.0,
      "background-opacity" : 1.0,
      "content" : "data(name)"
    }
  }, {
    "selector" : "node:selected",
    "css" : {
      "background-color" : "rgb(255,255,0)"
    }
  }, {
    "selector" : "edge",
    "css" : {
      "target-arrow-color" : "rgb(0,0,0)",
      "source-arrow-color" : "rgb(0,0,0)",
      "font-family" : "Dialog.plain",
      "font-weight" : "normal",
      "line-color" : "rgb(0,153,0)",
      "color" : "rgb(0,0,0)",
      "target-arrow-shape" : "none",
      "source-arrow-shape" : "none",
      "line-style" : "solid",
      "font-size" : 10,
      "text-opacity" : 1.0,
      "content" : "",
      "width" : 2.0,
      "opacity" : 1.0
    }
  }, {
    "selector" : "edge:selected",
    "css" : {
      "line-color" : "rgb(255,0,0)"
    }
  } ]
}, {
  "format_version" : "1.0",
  "generated_by" : "cytoscape-3.7.1",
  "target_cytoscapejs_version" : "~2.1",
  "title" : "Sample3",
  "style" : [ {
    "selector" : "node",
    "css" : {
      "border-width" : 8.0,
      "height" : 20.0,
      "color" : "rgb(206,206,206)",
      "text-opacity" : 1.0,
      "text-valign" : "bottom",
      "text-halign" : "right",
      "background-color" : "rgb(61,154,255)",
      "border-color" : "rgb(255,255,255)",
      "border-opacity" : 1.0,
      "font-size" : 14,
      "font-family" : "SansSerif.plain",
      "font-weight" : "normal",
      "shape" : "ellipse",
      "width" : 20.0,
      "background-opacity" : 1.0,
      "content" : "data(name)"
    }
  }, {
    "selector" : "node:selected",
    "css" : {
      "background-color" : "rgb(255,255,0)"
    }
  }, {
    "selector" : "edge",
    "css" : {
      "target-arrow-color" : "rgb(0,0,0)",
      "source-arrow-color" : "rgb(0,0,0)",
      "font-family" : "SansSerif.plain",
      "font-weight" : "normal",
      "line-color" : "rgb(255,255,255)",
      "color" : "rgb(0,0,0)",
      "target-arrow-shape" : "none",
      "source-arrow-shape" : "none",
      "line-style" : "solid",
      "font-size" : 10,
      "text-opacity" : 1.0,
      "content" : "",
      "width" : 2.0,
      "opacity" : 1.0
    }
  }, {
    "selector" : "edge:selected",
    "css" : {
      "line-color" : "rgb(255,0,0)"
    }
  } ]
}, {
  "format_version" : "1.0",
  "generated_by" : "cytoscape-3.7.1",
  "target_cytoscapejs_version" : "~2.1",
  "title" : "Solid",
  "style" : [ {
    "selector" : "node",
    "css" : {
      "border-width" : 0.0,
      "height" : 40.0,
      "color" : "rgb(0,0,0)",
      "text-opacity" : 1.0,
      "text-valign" : "center",
      "text-halign" : "center",
      "background-color" : "rgb(102,102,102)",
      "border-color" : "rgb(0,0,0)",
      "border-opacity" : 1.0,
      "font-size" : 14,
      "font-family" : "Dialog.plain",
      "font-weight" : "normal",
      "shape" : "ellipse",
      "width" : 40.0,
      "background-opacity" : 1.0,
      "content" : "data(name)"
    }
  }, {
    "selector" : "node:selected",
    "css" : {
      "background-color" : "rgb(255,255,0)"
    }
  }, {
    "selector" : "edge",
    "css" : {
      "target-arrow-color" : "rgb(0,0,0)",
      "source-arrow-color" : "rgb(0,0,0)",
      "font-family" : "Dialog.plain",
      "font-weight" : "normal",
      "line-color" : "rgb(204,204,204)",
      "color" : "rgb(0,0,0)",
      "target-arrow-shape" : "none",
      "source-arrow-shape" : "none",
      "line-style" : "solid",
      "font-size" : 10,
      "text-opacity" : 1.0,
      "width" : 12.0,
      "opacity" : 1.0,
      "content" : "data(interaction)"
    }
  }, {
    "selector" : "edge:selected",
    "css" : {
      "line-color" : "rgb(255,0,0)"
    }
  } ]
}, {
  "format_version" : "1.0",
  "generated_by" : "cytoscape-3.7.1",
  "target_cytoscapejs_version" : "~2.1",
  "title" : "Universe",
  "style" : [ {
    "selector" : "node",
    "css" : {
      "border-width" : 0.0,
      "height" : 40.0,
      "color" : "rgb(255,255,255)",
      "text-opacity" : 1.0,
      "text-valign" : "center",
      "text-halign" : "center",
      "background-color" : "rgb(0,0,0)",
      "border-color" : "rgb(0,0,0)",
      "border-opacity" : 1.0,
      "font-size" : 18,
      "font-family" : "Monospaced.plain",
      "font-weight" : "normal",
      "shape" : "ellipse",
      "width" : 40.0,
      "background-opacity" : 1.0,
      "content" : "data(name)"
    }
  }, {
    "selector" : "node:selected",
    "css" : {
      "background-color" : "rgb(255,255,0)"
    }
  }, {
    "selector" : "edge",
    "css" : {
      "target-arrow-color" : "rgb(0,0,0)",
      "source-arrow-color" : "rgb(0,0,0)",
      "font-family" : "Dialog.plain",
      "font-weight" : "normal",
      "line-color" : "rgb(153,153,153)",
      "color" : "rgb(0,0,0)",
      "target-arrow-shape" : "none",
      "source-arrow-shape" : "none",
      "line-style" : "dashed",
      "font-size" : 10,
      "text-opacity" : 1.0,
      "content" : "",
      "width" : 2.0,
      "opacity" : 1.0
    }
  }, {
    "selector" : "edge:selected",
    "css" : {
      "line-color" : "rgb(255,0,0)"
    }
  } ]
}, {
  "format_version" : "1.0",
  "generated_by" : "cytoscape-3.7.1",
  "target_cytoscapejs_version" : "~2.1",
  "title" : "Gradient1",
  "style" : [ {
    "selector" : "node",
    "css" : {
      "border-width" : 0.0,
      "height" : 30.0,
      "color" : "rgb(204,204,204)",
      "text-opacity" : 1.0,
      "text-valign" : "bottom",
      "text-halign" : "right",
      "background-color" : "rgb(0,0,0)",
      "border-color" : "rgb(0,0,0)",
      "border-opacity" : 1.0,
      "font-size" : 8,
      "font-family" : "SansSerif.plain",
      "font-weight" : "normal",
      "shape" : "ellipse",
      "width" : 30.0,
      "background-opacity" : 1.0,
      "content" : "data(name)"
    }
  }, {
    "selector" : "node:selected",
    "css" : {
      "background-color" : "rgb(255,255,0)"
    }
  }, {
    "selector" : "edge",
    "css" : {
      "target-arrow-color" : "rgb(0,0,0)",
      "source-arrow-color" : "rgb(0,0,0)",
      "font-family" : "SansSerif.plain",
      "font-weight" : "normal",
      "line-color" : "rgb(102,102,102)",
      "color" : "rgb(0,0,0)",
      "target-arrow-shape" : "none",
      "source-arrow-shape" : "none",
      "line-style" : "solid",
      "font-size" : 10,
      "text-opacity" : 1.0,
      "content" : "",
      "width" : 1.0,
      "opacity" : 1.0
    }
  }, {
    "selector" : "edge:selected",
    "css" : {
      "line-color" : "rgb(255,0,0)"
    }
  } ]
} ]