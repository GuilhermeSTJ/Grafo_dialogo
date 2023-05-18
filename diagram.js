var $ = go.GraphObject.make;


diagram = $(go.Diagram,"diagram",{
  "grid.visible" : true, // Faz o grip ficar visivel
  //"grid.gridCellSize": new go.Size(10, 10),
  //"draggingTool.dragsLink": true, // 
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

diagram.grid =
  $(go.Panel, go.Panel.Grid,  // or "Grid"
    { gridCellSize: new go.Size(50, 50) },
    $(go.Shape, "LineH", { stroke: "lightblue" }),
    $(go.Shape, "LineV", { stroke: "lightblue" })
  );

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


function nodeStyle() {
  return [
    new go.Binding("location", "loc", go.Point.parse).makeTwoWay(go.Point.stringify),
    {
      locationSpot: go.Spot.Center
    }
  ];
}

function load() {
  Modelo = prompt('Coloque os dados aqui:');
  diagram.model = go.Model.fromJson(Modelo);
}


function save() {
  texto = diagram.model.toJson();
  diagram.isModified = false;
  console.log(texto);

var blob = new Blob([texto], {
    type: "text/plain;charset=utf-8",
});
saveAs(blob, "saida.json");
}

//Cria o template do nó responsavel pelo Script
diagram.nodeTemplateMap.add("Script",
$(go.Node, "Auto",nodeStyle(),{
  fromSpot: go.Spot.Right, toSpot:go.Spot.Left
},
  $(go.Panel, "Position", {
    name:"MAIN"
  },
  $(go.Shape,"Circle",{ // Porta que sai links
    desiredSize: new go.Size(30,30), position: new go.Point(185,85), fill: "GreenYellow",
    portId: "Dialogo_out", fromLinkable: true, cursor: "pointer",
    stroke: null}),
    
    $(go.Shape,"Circle",{ // Porta que links se conectam
      desiredSize: new go.Size(30,30), position: new go.Point(-15,85), fill: "DarkRed",
      portId: "Dialogo_in", toLinkable: true, stroke: null}),

    $(go.Shape,"RoundedRectangle",{ // Parte do nome
      position: new go.Point(0,0),fill: "LightSlateGrey ",
      desiredSize: new go.Size(200, 40),stroke: null}),
      
    //Parte que contorna o texto e serve com porta de entrada 
    $(go.Shape,"RoundedRectangle",{ 
      position: new go.Point(0,30),fill: "LightSlateGrey ",desiredSize: new go.Size(200, 170),
      stroke: null}),

    //Parte que adequa a entrada de texto
    $(go.Shape,"RoundedRectangle",{
      position: new go.Point(5,35),fill: "lightgray",desiredSize: new go.Size(190, 160)}),

    //Parte que cerca o nome
      $(go.Shape,"RoundedRectangle",{
      position: new go.Point(100,8),fill: "DarkSlateGray",desiredSize: new go.Size(80, 20), stroke: null}),

    $(go.TextBlock, "Nome script:", {
      editable:true, position: new go.Point(10,10), font: "bold 10pt FontAwesome", stroke: "MintCream" }),

    //Variavel correspondente ao nome.
    $(go.TextBlock, "-----------",
      { position: new go.Point(102, 10),height: 20, width: 78, editable: true , stroke: "MintCream"  },
      new go.Binding("text", "key").makeTwoWay()
      ),

    //Bloco de texto onde recebera os comandos
    $(go.TextBlock, "",
      { position: new go.Point(20,50), editable: true, desiredSize: new go.Size(160, 130) },
      new go.Binding("text").makeTwoWay()
    )
)));

diagram.nodeTemplateMap.add("Dialogo",
  $(go.Node, "Auto",nodeStyle(),{
    fromSpot: go.Spot.Right, toSpot: go.Spot.Left,
  },
    $(go.Panel, "Position",

      $(go.Shape,"Circle",{ // Porta que sai links
        desiredSize: new go.Size(30,30), position: new go.Point(185,85), fill: "GreenYellow",
        portId: "Script_out", fromLinkable: true, cursor: "pointer",
        stroke: null}),

      $(go.Shape,"Circle",{ // Porta que links se conectam
        desiredSize: new go.Size(30,30), position: new go.Point(-15,85), fill: "DarkRed",
        portId: "Script_in", toLinkable: true,stroke: null}),
      
      $(go.Shape,"RoundedRectangle",{ // parte que vem o nome
      position: new go.Point(0,0),fill: "darkslategray",width:200, height: 200,stroke: null}),
      
      $(go.Shape,"Rectangle",{ // parte esquerda Relacionada ao input
        position: new go.Point(5,30),fill: "lemonchiffon",width:94, height: 165, stroke: null}),
        
      $(go.Shape,"Rectangle",{ // parte direita Relacionada ao output
        position: new go.Point(101,30),fill: "lightseagreen",width:94, height: 165, stroke: null}),
          
          //Parte que cerca o nome
      $(go.Shape,"RoundedRectangle",{
        position: new go.Point(100,6  ),fill: "LightGray",desiredSize: new go.Size(80, 20), stroke: null}),        

      $(go.TextBlock, "Nome Dialogo:", {
        editable:true, position: new go.Point(10,10), stroke: "white", font: "10pt FontAwesome" }),

      $(go.TextBlock, "-----------",new go.Binding("text", "key"),
        { position: new go.Point(103, 10), editable: true,height: 20, width: 78 },
        new go.Binding("text", "key").makeTwoWay()
        ),
      
      //Texto relacionado ao input
      $(go.TextBlock, "",
      { position: new go.Point(7,33), editable: true, desiredSize: new go.Size(90, 160) },
      new go.Binding("text","input").makeTwoWay(),
      ),

      //Texto relacionado ao output
      $(go.TextBlock, "",
      { position: new go.Point(104,33), editable: true, desiredSize: new go.Size(90, 160) },
      new go.Binding("text","output").makeTwoWay()
      )
)));


diagram.nodeTemplateMap.add("Inicia",
$(go.Node, "Auto",nodeStyle(),{
  fromSpot: go.Spot.Right, toSpot:go.Spot.Left, 
  resizable:true
},
  $(go.Panel, "Position", {
    name:"MAIN"
  },
    $(go.Shape,"Rectangle",{ 
      desiredSize: new go.Size(60,20), position: new go.Point(90,50), fill: "GreenYellow",
      portId: "Dialogo_out", fromLinkable: true, cursor: "pointer",
      stroke: null}), 
    $(go.Shape,"Circle",{ 
      desiredSize: new go.Size(120,120), position: new go.Point(0,0), fill: "Blue", stroke: null}), 
    $(go.TextBlock, "INICIO", {
      editable:true, position: new go.Point(25,45), stroke: "white", font: "20pt FontAwesome" }),
  )
));

diagram.nodeTemplateMap.add("Fim",
$(go.Node, "Auto",nodeStyle(),{
  fromSpot: go.Spot.Right, toSpot:go.Spot.Left, 
},
  $(go.Panel, "Position", {
    name:"MAIN"
  },
    $(go.Shape,"Rectangle",{ 
      desiredSize: new go.Size(60,20), position: new go.Point(-30,50), fill: "DarkRed",
      portId: "Script_in", toLinkable: true,stroke: null,
      stroke: null}), 
    $(go.Shape,"Circle",{ 
      desiredSize: new go.Size(120,120), position: new go.Point(0,0), fill: "Red", stroke: null}),
    $(go.TextBlock, "  FIM", {
      editable:true, position: new go.Point(40,45), stroke: "white", font: "20pt FontAwesome" }),
),
));

diagram.linkTemplate =
  $(go.Link,
    { corner:10, routing: go.Link.AvoidsNodes, curve:go.Link.JumpOver, fromEndSegmentLength: 30,toEndSegmentLength: 30 }, 
    $(go.Shape, { strokeWidth: 4 }),
    $(go.Shape, { toArrow: "Standard", scale:2 })
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
$(go.Palette, "Palette",  //Define em qual div vai ser colocado a palette
  {
    initialScale: 0.4,
    nodeTemplateMap: diagram.nodeTemplateMap,
    model: new go.GraphLinksModel([  
      {
        category: "Inicia"
      },
      {
        category: "Fim"
      },
      { 
        category: "Script",
      },
      { 
        category: "Dialogo",
       },
    ]),
  });
  
  myPalette.grid.visible = false;
