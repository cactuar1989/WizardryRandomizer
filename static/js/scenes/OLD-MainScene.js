class MainScene extends Phaser.Scene {
    constructor() {
        super({
            key: "MainScene"
        });
    }
    // called on scene start and restart
    init(data) {
        //character.level = data.level;
        // deep copy of array so changes aren't kept after restart()
        maze = [];
        var map = "level_" + character.level;
        for (var i = 0; i < eval(map).length; i++) {
            // use eval() so we are getting the object instead of just working with the string of the name
            maze[i] = eval(map)[i].slice();
        }
        // set up player
        if (character.level === 0) {
            character.inventory = [];
            direction = 2;
            playerX = 2;
            playerY = 2;
        }
    }
    preload() {
        defaultScene = this;
        // load audio files
        doorSounds.forEach(function(value) {
            // loads each item from doorSounds in game.js array as value
            this.load.audio(value,"static/assets/sounds/" + value + ".ogg");
        }, this);
        this.load.audio("wiz2door", "static/assets/sounds/wiz2door.wav");
        // background
        this.load.image("background", "static/assets/background.png");
        this.load.image("box", "static/assets/box.png");
        // walls
        this.load.image("leftWall", "static/assets/leftWall.png");
        this.load.image("leftCornerWall", "static/assets/leftCornerWall.png");
        this.load.image("farLeftWall", "static/assets/farLeftWall.png");
        this.load.image("rightWall", "static/assets/rightWall.png");
        this.load.image("rightCornerWall", "static/assets/rightCornerWall.png");
        this.load.image("farRightWall", "static/assets/farRightWall.png");
        this.load.image("closeCenterWall", "static/assets/closeCenterWall.png");
        this.load.image("farCenterWall", "static/assets/farCenterWall.png");
        // doors
        this.load.image("leftDoor", "static/assets/leftDoor.png");
        this.load.image("leftCornerDoor", "static/assets/leftCornerDoor.png");
        this.load.image("farLeftDoor", "static/assets/farLeftDoor.png");
        this.load.image("closeLeftDoor", "static/assets/closeLeftDoor.png");
        this.load.image("rightDoor", "static/assets/rightDoor.png");
        this.load.image("rightCornerDoor", "static/assets/rightCornerDoor.png");
        this.load.image("farRightDoor", "static/assets/farRightDoor.png");
        this.load.image("closeRightDoor", "static/assets/closeRightDoor.png");
        this.load.image("closeCenterDoor", "static/assets/closeCenterDoor.png");
        this.load.image("farCenterDoor", "static/assets/farCenterDoor.png");

        this.load.image("farLeftItem", "static/assets/farLeftItem.png");
        this.load.image("farRightItem", "static/assets/farRightItem.png");
        this.load.image("farCenterItem", "static/assets/farCenterItem.png");
        this.load.image("closeCenterItem", "static/assets/closeCenterItem.png");

        this.load.audio("mazeMusic", "static/assets/music/Wiz3Maze.mp3");
    }
    create() {
        if (bgmusic === null) {
            // initialize music once then just keep it playing as we progress through the levels
            bgmusic = this.sound.add("mazeMusic", {volume: 0.75});
            bgmusic.loop = true;
            bgmusic.play();
        }
        // add listener for pointer/swipe click and drag events
        this.input.on("pointerdown", function(event) {
            pointerStartX = event.downX;
            pointerStartY = event.downY;
        }, this);
        this.input.on("pointerup", function(event) {
            // clear message popups
            //messageFlag = false;
            pointerEndX = event.upX;
            pointerEndY = event.upY;
            // left pointer drag is < 0
            if ((pointerEndX - pointerStartX) < -MIN_SWIPE_DISTANCE) {
                // swipe left
                turnLeft();
            } else if ((pointerEndX - pointerStartX) > MIN_SWIPE_DISTANCE) {
                // swipe right
                turnRight();
            } else if ((pointerEndY - pointerStartY) < -MIN_SWIPE_DISTANCE) {
                // swipe up
                moveUp();
            } else if ((pointerEndY - pointerStartY) > MIN_SWIPE_DISTANCE) {
                // swipe down
                moveDown();
            } else {
                interact();
            }
        }, this);
        // add listener for keyboard press event
        this.input.keyboard.on("keydown", function(event) {
            // clear message popups by pressing any key
            //messageFlag = false;
            //console.log(event.code);
            switch(event.code) {
                case "Space":
                    interact();
                    break;
                case "KeyA":
                case "ArrowLeft":
                    turnLeft();
                    break;
                case "KeyD":
                case "ArrowRight":
                    turnRight();
                    break;
                case "KeyW":
                case "ArrowUp":
                    moveUp();
                    break;
                case "KeyS":
                case "ArrowDown":
                    moveDown();
                    break;
                case "KeyC":
                    //messageFlag = true;
                    //message = "Popup";
                    var waiting = true;
                    dialog("Testing dialog popups\nLine two\nMuch longer line for test!");
                    break;
                case "KeyI":
                    console.log(character.inventory);
                    break;
                case "KeyK":
                    /*
                    if (maze[playerY][playerX] == " ") {
                        maze[playerY][playerX] = "K";
                    } else {
                        pickupItem();
                    }
                    */
                    break;
                case "KeyR":
                    //this.scene.restart();
                    break;
            }
        }, this);
        // background
        this.add.image(0, 0, "background").setOrigin(0,0).setDisplaySize(config.width,config.height);
        // sounds
        doorSounds.forEach(function(value) {
            // adds each item from doorSounds array
            this.sound.add(value);
        }, this);
        // create countdown timer
        this.initialTime = 0; // starting timer value
        // each 1000 ms call timerUpdate
        timerEvent = this.time.addEvent({
            delay: 1000,
            callback: timerUpdate, // countdown timer
            callbackScope: this,
            loop: true
        });
        soundTimer = this.time.addEvent({
            delay: getRandomInt(10, 60) * 1000, // play sound every 10 - 60 seconds
            callback: function(){
                // play door + random # from 0 to length of array ( - 1 because we started at zero )
                this.sound.play("door" + getRandomInt(0,doorSounds.length - 1), {volume: 0.50});
            },
            callbackScope: this,
            loop: true
        });
    }

    update() {
        // get surrounding cells as a matrix
        getSurroundings();

        // rotate matrix if required to always have player facing North in grid
        // 0 = North, 1 = Eeast, 2 = South, 3 = West
        if (direction == 0) {
            // grid doesn't need rotation
        } else if (direction == 1) {
            // rotate 3 times for 270 degress CW
            grid = rotateGrid(rotateGrid(rotateGrid(grid)));
        } else if (direction == 2) {
            // rotate 180
            grid = rotateGrid(rotateGrid(grid));
        } else if (direction == 3) {
            // rotate 90 CW
            grid = rotateGrid(grid);
        }
        // sample grid
        /*
        ['#', '#', ' ', '#', '#']
        ['#', '#', ' ', '#', '#']
        ['#', '#', ' ', 'L', ' ']
        ['#', '#', '#', '#', '#']
        ['#', '#', '#', '#', '#']
        */
        // remove all images from scene
        this.add.displayList.removeAll();
        // background
        this.add.image(0, 0, "background").setOrigin(0,0).setDisplaySize(config.width,config.height);
        // add surroundings
        var opposite_dir = ((direction + 2) % 4);
        if (wallChars.includes(grid[0][1])) {
            this.add.image(0, 0, "farLeftWall").setOrigin(0,0).setDisplaySize(config.width,config.height);
        } else if (doorChars.includes(grid[0][1])) {
            // we know it"s a door but is it N, E, S, or W facing
            if (grid[0][1][1] == opposite_dir) {
                this.add.image(0, 0, "farLeftDoor").setOrigin(0,0).setDisplaySize(config.width,config.height);
            }
        }
        if (items.includes(grid[1][1])) {
            this.add.image(0, 0, "farLeftItem").setOrigin(0,0).setDisplaySize(config.width,config.height);
        }
        if (wallChars.includes(grid[0][2])) {
            this.add.image(0, 0, "farCenterWall").setOrigin(0,0).setDisplaySize(config.width,config.height);
        } else if (doorChars.includes(grid[0][2])) {
            // we know it's a door but is it N, E, S, or W facing
            if (grid[0][2][1] == opposite_dir) {
                this.add.image(0, 0, "farCenterDoor").setOrigin(0,0).setDisplaySize(config.width,config.height);
            }
        }
        if (items.includes(grid[1][2])) {
            this.add.image(0, 0, "farCenterItem").setOrigin(0,0).setDisplaySize(config.width,config.height);
        }
        if (wallChars.includes(grid[0][3])) {
            this.add.image(0, 0, "farRightWall").setOrigin(0,0).setDisplaySize(config.width,config.height);
        } else if (doorChars.includes(grid[0][3])) {
            // we know it's a door but is it N, E, S, or W facing
            if (grid[0][3][1] == opposite_dir) {
                this.add.image(0, 0, "farRightDoor").setOrigin(0,0).setDisplaySize(config.width,config.height);
            }
        }
        if (items.includes(grid[1][3])) {
            this.add.image(0, 0, "farRightItem").setOrigin(0,0).setDisplaySize(config.width,config.height);
        }
        if (wallChars.includes(grid[1][1])) {
            this.add.image(0, 0, "leftCornerWall").setOrigin(0,0).setDisplaySize(config.width,config.height);
        } else if (doorChars.includes(grid[1][1])) {
            if (grid[1][1][1] ==  ((direction + 1) % 4)) {
                this.add.image(0, 0, "leftCornerDoor").setOrigin(0,0).setDisplaySize(config.width,config.height);
            }
            if (grid[1][1][1] == ((direction + 2) % 4)) {
                this.add.image(0, 0, "closeLeftDoor").setOrigin(0,0).setDisplaySize(config.width,config.height);
            }
        }
        if (wallChars.includes(grid[1][3])) {
            this.add.image(0, 0, "rightCornerWall").setOrigin(0,0).setDisplaySize(config.width,config.height);
        } else if (doorChars.includes(grid[1][3])) {
             if (grid[1][3][1] ==  ((direction + 3) % 4)) {
                this.add.image(0, 0, "rightCornerDoor").setOrigin(0,0).setDisplaySize(config.width,config.height);
             }
             if (grid[1][3][1] == ((direction + 2) % 4)) {
                this.add.image(0, 0, "closeRightDoor").setOrigin(0,0).setDisplaySize(config.width,config.height);
            }
        }
        if (wallChars.includes(grid[2][1])) {
            this.add.image(0, 0, "leftWall").setOrigin(0,0).setDisplaySize(config.width,config.height);
        } else if (doorChars.includes(grid[2][1])) {
            if (grid[2][1][1] == ((direction + 1) % 4)) {
                this.add.image(0, 0, "leftDoor").setOrigin(0,0).setDisplaySize(config.width,config.height);
            }
        }
        if (wallChars.includes(grid[2][3])) {
            this.add.image(0, 0, "rightWall").setOrigin(0,0).setDisplaySize(config.width,config.height);
        } else if (doorChars.includes(grid[2][3])) {
            if (grid[2][3][1] == ((direction + 3) % 4)) {
                this.add.image(0, 0, "rightDoor").setOrigin(0,0).setDisplaySize(config.width,config.height);
            }
        }
        if (wallChars.includes(grid[1][2])) {
            this.add.image(0, 0, "closeCenterWall").setOrigin(0,0).setDisplaySize(config.width,config.height);
        } else if (doorChars.includes(grid[1][2])) {
            if (grid[1][2][1] == opposite_dir) {
                this.add.image(0, 0, "closeCenterDoor").setOrigin(0,0).setDisplaySize(config.width,config.height);
            }
            if (grid[1][2][1] == direction) {
                this.add.image(0, 0, "farCenterDoor").setOrigin(0,0).setDisplaySize(config.width,config.height);
            }
        }
        if (doorChars.includes(grid[2][2])) {
            if (grid[2][2][1] == (direction)) {
                this.add.image(0, 0, "closeCenterDoor").setOrigin(0,0).setDisplaySize(config.width,config.height);
            }
            if (grid[2][2][1] == ((direction + 3) % 4)) {
                this.add.image(0, 0, "leftDoor").setOrigin(0,0).setDisplaySize(config.width,config.height);
            }
            if (grid[2][2][1] == ((direction + 1) % 4)) {
                this.add.image(0, 0, "rightDoor").setOrigin(0,0).setDisplaySize(config.width,config.height);
            }
        }
        if (items.includes(grid[2][2])) {
            this.add.image(0, 0, "closeCenterItem").setOrigin(0,0).setDisplaySize(config.width,config.height);
        }
/*
        if (grid[0][1] == "K") {
            this.add.image(config.width * 0.5, config.height * 0.7, "key");
        }
        if (grid[1][1] == "K") {
            this.add.image(config.width * 0.5, config.height * 0.9, "closeKey");
        }
*/
        // check the space you are standing on for ending
        if (grid[2][2] == "E") {
            game.scene.stop("MainScene");
            game.scene.start("EndScene", { music: bgmusic });
        }
        // check for stairs
        if (grid[2][2] == "S") {
            dialog("You move deeper into the dungeon");
            game.scene.start("LevelChangeScene");
        }

        // add timer text (xPos, yPos, text)
        timerText = this.add.text(20, 10, "Time: " + formatTime(this.initialTime), { font: "16px prstart" });
        // add Compass text, getDirection returns N,E,S, or W as string
        if (character.compass) {
            this.add.text(config.width - 40, 10, getDirection(), { font: "18px prstart" });
        }
        if (character.gps) {
            this.add.text(config.width - 140, 35, playerX + "," + playerY, { font: "12px prstart" });
        }
        // print level number
        this.add.text(config.width - 140, 10, "Level: " + character.level, { font: "10px prstart" });
//        if (messageFlag == true) {
//            // create the text in a var so we can see the bounds
//            var temp = this.add.text(-100, -100, message, { font: "12px prstart" });
//            var bounds = temp.getBounds();
//            //console.log(bounds);
//            // add box around message
//            this.add.image(bounds.x-10,bounds.y-3,"box").setOrigin(0,0).setDisplaySize(bounds.width+20,bounds.height+6);
//            // add message on top of box
//            this.add.text(20, 35, message, { font: "10px prstart" });
//        }
    }
}

function turnLeft() {
    if (direction == 0) {
        direction = 3;
    } else {
        direction -= 1;
    }
}

function turnRight() {
    if (direction == 3) {
        direction = 0;
    } else {
        direction += 1;
    }
}

function moveUp() {
    // grid space directly in front of char is row 1, column 2
    var can_move = true;
    if (wallChars.includes(grid[1][2])) {
        can_move = false; 
    }
    if (doorChars.includes(grid[1][2])) {
        if (grid[1][2][1] == ((direction + 2) % 4)) {
            can_move = false; 
        }
    }
    if (doorChars.includes(grid[2][2])) {
        if (grid[2][2][1] == direction) {
            can_move = false; 
        }
    }
    if (can_move === true) {
        // if facing a wall, don't move forward
        if (direction == 0) {
            playerY -= 1;
        } else if (direction == 1) {
            playerX += 1;
        } else if (direction == 2) {
            playerY += 1;
        } else if (direction == 3) {
            playerX -= 1;
        }
    }
}

function moveDown() {
    // grid space directly behind char is row 3, column 2
    var can_move = true;
    if (wallChars.includes(grid[3][2])) {
        can_move = false; 
    }
    if (doorChars.includes(grid[3][2])) {
        if (grid[3][2][1] == (direction)) {
            can_move = false; 
        }
    }
    if (doorChars.includes(grid[2][2])) {
        if (grid[2][2][1] == ((direction + 2) % 4)) {
            can_move = false; 
        }
    }
    //if (grid[3][2] != '#' && grid[3][2] != 'D') {
        // if facing a wall, don't move backward
    if (can_move === true) {
        if (direction == 0) {
            playerY += 1;
        } else if (direction == 1) {
            playerX -= 1;
        } else if (direction == 2) {
            playerY -= 1;
        } else if (direction == 3) {
            playerX += 1;
        }
    }
}

function interact() {
    // if facing door
    var standing_on = grid[2][2];
    var facing = grid[1][2];
    if (doorChars.includes(facing)) {
        if (facing[1] == ((direction + 2) % 4)) {
            defaultScene.sound.play("wiz2door");
            if (direction == 0) {
                playerY -= 1;
            } else if (direction == 1) {
                playerX += 1;
            } else if (direction == 2) {
                playerY += 1;
            } else if (direction == 3) {
                playerX -= 1;
            }
        }
    }
    // if standing on tile with door
    else if (doorChars.includes(standing_on)) {
        if (standing_on[1] == direction) {
            defaultScene.sound.play("wiz2door");
            if (direction == 0) {
                playerY -= 1;
            } else if (direction == 1) {
                playerX += 1;
            } else if (direction == 2) {
                playerY += 1;
            } else if (direction == 3) {
                playerX -= 1;
            }
        }
    }
    else if (standing_on === "C") {
        character.compass = true;
        dialog("You found a compass");
    }
    else if (standing_on === "G") {
        character.gps = true;
        dialog("You found a GPS");
    }
    else {
        dialog("There is nothing here.");
    }
}

function pickupItem(item) {
    /*
    // remove item from map
    maze[playerY][playerX] = " ";
    // add item to inventory array
    character.inventory.push(item);
    // set message popup flag = true
    messageFlag = true;
    switch(item) {
        case "K":
            message = "You found a key";
            break;
        default:
            message = "You found an item (" + item + ")";
            break;
    }
    */
}

function useItem(item) {
    /*
    var i = character.inventory.indexOf(item);
    if (i > -1) {
        character.inventory.splice(i, 1);
    }
    */
}

function getSurroundings() {
    // get the cells around the player instead of loading the entire map when we add walls
    // grid is 5 x 5 matrix with player in center
    var row = playerY;
    var col = playerX;
    
    grid = [
        [maze[row-2][col-2], maze[row-2][col-1], maze[row-2][col-0], maze[row-2][col+1], maze[row-2][col+2]],
        [maze[row-1][col-2], maze[row-1][col-1], maze[row-1][col-0], maze[row-1][col+1], maze[row-1][col+2]],
        [maze[row-0][col-2], maze[row-0][col-1], maze[row-0][col-0], maze[row-0][col+1], maze[row-0][col+2]],
        [maze[row+1][col-2], maze[row+1][col-1], maze[row+1][col-0], maze[row+1][col+1], maze[row+1][col+2]],
        [maze[row+2][col-2], maze[row+2][col-1], maze[row+2][col-0], maze[row+2][col+1], maze[row+2][col+2]],
    ];
}

/*
function getFacingCell() {
    var x = 0, y = 0;
    switch(direction) {
        case 0:
            // facing North
            x = playerX;
            y = playerY - 1;
            break;
        case 1:
            // facing East
            x = playerX + 1;
            y = playerY;
            break;
        case 2:
            // facing South
            x = playerX;
            y = playerY + 1;
            break;
        case 3:
            // facing West
            x = playerX - 1;
            y = playerY;
            break;
    }
    return [x,y];
}
*/

function rotateGrid(matrix) {
    // Copy the original matrix
    var origMatrix = matrix.slice();
    for(var i=0; i < matrix.length; i++) {
        // Map each row entry to its rotated value
        var row = matrix[i].map(function(x, j) {
            var k = (matrix.length - 1) - j;
            return origMatrix[k][i];
        });
        matrix[i] = row;
    }
    return matrix;
}

function formatTime(seconds){
    // Minutes
    var minutes = Math.floor(seconds/60);
    // Seconds
    var partInSeconds = seconds%60;
    // Adds left zeros to seconds
    partInSeconds = partInSeconds.toString().padStart(2,"0");
    // Returns formated time
    return `${minutes}:${partInSeconds}`;
}

function timerUpdate(){
    this.initialTime += 1; // add one second
    //if (this.initialTime > 0) {
        //this.initialTime -= 1; // subtract one second
    //}
}

function getDirection(){
    if (direction == 0){
        return "N";
    } else if (direction == 1){
        return "E";
    } else if (direction == 2){
        return "S";
    } else if (direction == 3){
        return "W";
    }
}

// returns a random int, min and max included
function getRandomInt(min, max){
    return Math.floor(Math.random() * (max - min + 1) ) + min;
}

function dialog(msg, lines) {
    defaultScene.scene.launch('DialogScene', { message: msg });
    defaultScene.scene.pause();
}