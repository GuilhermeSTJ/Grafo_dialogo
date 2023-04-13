var $ = go.GraphObject.make;

diagram = $(go.Diagram,"diagram",{
  "grid.visible" : true, // Faz o grip ficar visivel
  "draggingTool.dragsLink": true, // 
  "draggingTool.isGridSnapEnabled": true,
  "resizingTool.isGridSnapEnabled" : true,
  "linkingTool.isUnconnectedLinkValid": true,
  "linkingTool.portGravity": 20,
  "relinkingTool.isUnconnectedLinkValid": true,
  "relinkingTool.portGravity": 20,
  "rotatingTool.handleAngle": 270,
  "rotatingTool.handleDistance": 30,
  "rotatingTool.snapAngleMultiple": 15,
  "rotatingTool.snapAngleEpsilon": 15,
  "undoManager.isEnabled": true
});

diagram.addDiagramListener("Modified", e => {
  var button = document.getElementById("SaveButton");
  if (button) button.disabled = !diagram.isModified;
  var idx = document.title.indexOf("*");
  if (diagram.isModified) {
    if (idx < 0) document.title += "*";
  } else {
    if (idx >= 0) document.title = document.title.slice(0, idx);
  }
});

function save() {
  document.getElementById("mySavedModel").value = diagram.model.toJson();
  diagram.isModified = false;
}
function load() {
  diagram.model = go.Model.fromJson(document.getElementById("mySavedModel").value);
}

//Cria o template do nó responsavel pelo Script
diagram.nodeTemplateMap.add("Script",
$(go.Node, "Auto",
  $(go.Panel, "Position",

    $(go.Shape,"RoundedRectangle",{ // Parte do nome
      position: new go.Point(0,0),fill: "lightblue",desiredSize: new go.Size(200, 40),stroke: null}),

    $(go.Shape,"Circle",{ // Porta que sai links
      desiredSize: new go.Size(30,30), position: new go.Point(185,85), fill: "GreenYellow",
      portId: "Dialogo_out", fromSpot: go.Spot.Right, fromLinkable: true, cursor: "pointer",
      stroke: null}),

    $(go.Shape,"Circle",{ // Porta que links se conectam
      desiredSize: new go.Size(30,30), position: new go.Point(-15,85), fill: "DarkRed",
      portId: "Dialogo_in",toSpot: go.Spot.Left, toLinkable: true, stroke: null}),

    //Parte que contorna o texto e serve com porta de entrada 
    $(go.Shape,"Rectangle",{ 
      position: new go.Point(0,30),fill: "blue",desiredSize: new go.Size(200, 170),
      stroke: null}),

    //Parte que adequa a entrada de texto
    $(go.Shape,"RoundedRectangle",{
      position: new go.Point(5,35),fill: "lightgray",desiredSize: new go.Size(190, 160)}),
    $(go.TextBlock, "Nome script:", {
      editable:true, position: new go.Point(10,10) }),

    //Variavel correspondente ao nome.
    $(go.TextBlock, "-----------", new go.Binding("text", "key"),
      { position: new go.Point(100, 10), editable: true }),

    //Bloco de texto onde recebera os comandos
    $(go.TextBlock, "",
      { position: new go.Point(20,50), editable: true, desiredSize: new go.Size(160, 130) })

)));

diagram.nodeTemplateMap.add("Dialogo",
  $(go.Node, "Auto",
    $(go.Panel, "Position",

    $(go.Shape,"RoundedRectangle",{ // parte que vem o nome
      position: new go.Point(0,0),fill: "SandyBrown",width:200, height: 40,stroke: null}),

    $(go.Shape,"Circle",{ // Porta que sai links
      desiredSize: new go.Size(30,30), position: new go.Point(185,85), fill: "GreenYellow",
      portId: "Script_out", fromSpot: go.Spot.Right, fromLinkable: true, cursor: "pointer",
      stroke: null}),

    $(go.Shape,"Circle",{ // Porta que links se conectam
      desiredSize: new go.Size(30,30), position: new go.Point(-15,85), fill: "DarkRed",
      portId: "Script_in", toSpot: go.Spot.Left, toLinkable: true,stroke: null}),

    $(go.Shape,"Rectangle",{ // parte esquerda Relacionada ao input
      position: new go.Point(0,30),fill: "#acedda",width:100, height: 170}),

    $(go.Shape,"Rectangle",{ // parte direita Relacionada ao output
      position: new go.Point(100,30),fill: "#acedda",width:100, height: 170}),

    $(go.TextBlock, "Nome Dialogo:", {
      editable:true, position: new go.Point(10,10) }),

    $(go.TextBlock, "-----------",new go.Binding("text", "key"),
    { position: new go.Point(100, 10), editable: true })


)));


diagram.linkTemplate =
  $(go.Link,
    { corner:10, routing: go.Link.AvoidsNodes },  // Bezier curve
    $(go.Shape),
    $(go.Shape, { toArrow: "Standard" })
  );

diagram.contextMenu =
  $("ContextMenu",
    $("ContextMenuButton",
      $(go.TextBlock, "Undo"),
      { click: (e, obj) => e.diagram.commandHandler.undo() },
      new go.Binding("visible", "", o => o.diagram.commandHandler.canUndo()).ofObject()),
    $("ContextMenuButton",
      $(go.TextBlock, "Redo"),
      { click: (e, obj) => e.diagram.commandHandler.redo() },
      new go.Binding("visible", "", o => o.diagram.commandHandler.canRedo()).ofObject()),
    // no binding, always visible button:
    
  );

myPalette =
$(go.Palette, "Palette",  // must name or refer to the DIV HTML element
  {
    initialScale: 0.4,
    nodeTemplateMap: diagram.nodeTemplateMap,  // share the templates used by myDiagram
    model: new go.GraphLinksModel([  // specify the contents of the Palette
      { 
        category: "Script",
      },
      { 
        category: "Dialogo" },
    ]),
  });
  window.addEventListener('DOMContentLoaded', init);