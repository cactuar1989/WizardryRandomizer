// our game's configuration
let config = {
    type: Phaser.AUTO,  //Phaser will decide how to render our game (WebGL or Canvas)
    width: 256*2, // game width
    height: 240*2, // game height, both are required even though we scale up to fit screen
    scale: {
        mode: Phaser.Scale.FIT,
        autoCenter: Phaser.Scale.CENTER_BOTH
    },
    physics: { arcade: { fps: 15 } },
    scene: [ BootScene, IntroScene, MainScene, EndScene, DialogScene, LevelChangeScene ],
    title: 'LOST',
    backgroundColor: '000000', // black bg color
    pixelArt: true,
    antiAlias: true
};

defaultScene = null;
bgmusic = null;
var game;
// create the game, and pass it the configuration
function startGame() {
    document.getElementById("start").remove();
    game = new Phaser.Game(config);
    resetPlayer();
}

var character = {
    level: 0,
    name: "Test",
    //inventory: ["B","A","K","E","D","A","L","A","S","K","A"]
    inventory: [],
    compass: false,
    gps: false
}
var playerX;
var playerY;
var direction; // 0 = North, 1 = Eeast, 2 = South, 3 = West
var initialTime;
//var bgmusic;

function resetPlayer() {
    character.level = 0;
    character.compass = false;
    character.gps = false;
    playerX = 0;
    playerY = 19;
    direction = 0;
    initialTime = 0;
}

var maze;
var levelChange;
//var facingWall;
//var wallChars = [ "#" ];
//var doorChars = [ "D", "L", "D0", "D1", "D2", "D3", "L0", "L1", "L2", "L3" ];
//var items = [ "K","?","C","G","E" ];
var doorSounds = [ "door0", "door1", "door2", "door3" ];
var wallImages = ["close_centerWall","close_leftWall","close_rightWall","close_adjacent_leftWall","close_adjacent_rightWall",
"far_centerWall","far_leftWall","far_rightWall","far_adjacent_leftWall","far_adjacent_rightWall"];
var doorImages = ["close_adjacent_leftDoor","close_adjacent_rightDoor","close_centerDoor","close_leftDoor","close_rightDoor",
"far_adjacent_leftDoor","far_adjacent_rightDoor","far_centerDoor","far_leftDoor","far_rightDoor"];
//var messageFlag;
//var message;
var timerText;
var timerEvent;
var soundTimer;

var pointerStartX, pointerStartY;
var pointerEndX, pointerEndY;
var MIN_SWIPE_DISTANCE = 75; // minimum distance to swipe/drage pointer to move player

var spaceBar;
var spaceReleased = false;
var hasPlayerMoved = false;
//var dialogMessage;
var sArr; // array for string to dialog
var maxl; // max length of dialog line
var inPrompt = false;
var inDialog = false;
var cursorUp = true;
var cursorY = 50;
var currentEvent;