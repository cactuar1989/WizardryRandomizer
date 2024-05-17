class MainScene extends Phaser.Scene {
    constructor() {
        super({
            key: "MainScene"
        });
    }
    // called on scene start and restart
    init() {
        // deep copy of array so changes aren't kept after restart()
        var map = "level_" + character.level;
        maze = eval(map);
        var events_map = "level_" + character.level + "_events";
        events = eval(events_map);
        /*
        var map = "level_" + character.level;
        for (var i = 0; i < eval(map).length; i++) {
            // use eval() so we are getting the object instead of just working with the string of the name
            maze[i] = eval(map)[i].slice();
        }
        */
        // set up player
        /*
        if (character.level === 0) {
            direction = 0;
            playerX = 0;
            playerY = 19;
        }
        */
        //playerSetup(character.level);
    }
    preload() {
        defaultScene = this;
        // load audio files
        doorSounds.forEach(function(value) {
            // loads each item from doorSounds in game.js array as value
            this.load.audio(value,"static/assets/sounds/" + value + ".ogg");
        }, this);
        this.load.audio("wiz2door", "static/assets/sounds/wiz2door.wav");
        this.load.audio("mazeMusic", "static/assets/music/Wiz3Maze.mp3");
        // background
        this.load.image("background", "static/assets/background.png");
        this.load.image("box", "static/assets/box.png");
        this.load.image("close_item", "static/assets/close_item.png");
        this.load.image("far_item", "static/assets/far_item.png");
        this.load.image("close_item_ceiling", "static/assets/close_item_ceiling.png");
        this.load.image("far_item_ceiling", "static/assets/far_item_ceiling.png");
        // wall and doors
        wallImages.forEach(function(value) {
            this.load.image(value,"static/assets/" + value + ".png");
        }, this);
        doorImages.forEach(function(value) {
            this.load.image(value,"static/assets/" + value + ".png");
        }, this);
        
        this.load.image("cursor", "static/assets/cursor.png");
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
        spaceBar = this.input.keyboard.addKey(Phaser.Input.Keyboard.KeyCodes.SPACE);
        this.input.keyboard.on("keydown", function(event) {
            switch(event.code) {
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
                case "KeyP":
                    dialog("Test dialog here");
                    inPrompt = true;
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
        //this.initialTime = 0; // starting timer value
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
        // remove all images from scene
        this.add.displayList.removeAll();
        // background
        this.add.image(0, 0, "background").setOrigin(0,0).setDisplaySize(config.width,config.height);

        // add timer text (xPos, yPos, text)
        timerText = this.add.text(20, 10, "Time: " + formatTime(initialTime), { font: "16px prstart" });
        // add Compass text, getDirection returns N,E,S, or W as string
        if (character.compass === true) {
            this.add.text(config.width - 40, 10, getDirection(), { font: "18px prstart" });
        }
        // coordinates
        if (character.gps === true) {
            this.add.text(config.width - 140, 35, playerX + "," + playerY, { font: "12px prstart" });
        }
        // print level number
        this.add.text(config.width - 140, 10, "Level: " + character.level, { font: "10px prstart" });

        var currentCell = maze[playerY][playerX];
        var facingCell;
        var farX;
        var farY;
        var adjLeft;
        var adjRight;
        var left;
        var right;
        if (direction == 0) {
            // facing north
            if (playerY > 0) {
                farY = playerY - 1;
            } else {
                farY = maze.length - 1;
            }
            farX = playerX;
        } else if (direction == 1) {
            // facing east
            farY = playerY;
            farX = (playerX + 1) % maze[0].length;

        } else if (direction == 2) {
            // facing south
            farX = playerX;
            farY = (playerY + 1) % maze.length;

        } else {
            // facing west
            farY = playerY;
            if (playerX > 0) {
                farX = playerX - 1;
            } else {
                farX = maze[0].length - 1;
            }
        }
        facingCell = maze[farY][farX];
        // getAdjacentTiles(row, col) return [adjLeftRow, adjLeftCol, adjRightRow, adjRightCol];
        var [adjLeftRow, adjLeftCol, adjRightRow, adjRightCol] = getAdjacentTiles(farY, farX);
        var [leftRow, leftCol, rightRow, rightCol] = getAdjacentTiles(playerY, playerX);
        adjLeft = maze[adjLeftRow][adjLeftCol];
        adjRight = maze[adjRightRow][adjRightCol];
        left = maze[leftRow][leftCol];
        right = maze[rightRow][rightCol];

        // processTile(tileCode, far, adjacent, left)
        processTile(adjLeft, true, true, true);
        processTile(adjRight, true, true, false);
        processTile(facingCell, true, false, false);
        if (eventCodes.includes(events[farY][farX])) {
            if (events[farY][farX] === "UP") {
                this.add.image(0, 0, "far_item_ceiling").setOrigin(0,0).setDisplaySize(config.width,config.height);
            } else {
                this.add.image(0, 0, "far_item").setOrigin(0,0).setDisplaySize(config.width,config.height);
            }
        }
        processTile(left, false, true, true);
        processTile(right, false, true, false);
        processTile(currentCell, false, false, false);
        //console.log(playerY + "," + playerX + " cell=" + maze[playerY][playerX] + " direction=" + direction + " facing=" + facingCell + " left=" + left + " right=" + right);
        if (events[playerY][playerX][0] === "W") {
            warpPlayer(events[playerY][playerX][1]);
        }
        if (eventCodes.includes(events[playerY][playerX])) {
            if (events[playerY][playerX] === "UP") {
                //this.add.image(0, 0, "close_item_ceiling").setOrigin(0,0).setDisplaySize(config.width,config.height);
            } else {
                this.add.image(0, 0, "close_item").setOrigin(0,0).setDisplaySize(config.width,config.height);
            }
            if (hasPlayerMoved === true) {
                doEvent(events[playerY][playerX]);
            }
        }
        // draw prompt box
        if (inPrompt && !inDialog) {
            this.add.image(38, 36, "box").setOrigin(0, 0).setDisplaySize(4*12+12, 2*12+18); // set for 12px prstart font
            this.add.text(60, 45, "Yes\nNo", { font: "12px prstart" });
            this.add.image(50, cursorY, "cursor").setScale(2);
        }
        // so you can't hold space bar to interact
        if (spaceBar.isDown) {
            if (spaceReleased === true) {
                interact();
                spaceReleased = false;
            }
        }
        if (spaceBar.isUp) {
            spaceReleased = true;
        }
        hasPlayerMoved = false;
    }
}

function turnLeft() {
    if (inPrompt) {
        return;
    }
    if (direction == 0) {
        direction = 3;
    } else {
        direction -= 1;
    }
    hasPlayerMoved = true;
}

function turnRight() {
    if (inPrompt) {
        return;
    }
    if (direction == 3) {
        direction = 0;
    } else {
        direction += 1;
    }
    hasPlayerMoved = true;
}

function moveUp() {
    if (inPrompt) {
        if (cursorUp === false) {
            cursorY -= 12;
            cursorUp = true;
        }
        return;
    }
    if (canMove === true) {
        // if facing a wall, don't move forward
        if (direction == 0) {
            if (playerY == 0) {
                playerY = maze.length - 1;
            } else {
                playerY -= 1;
            }
        } else if (direction == 1) {
            playerX = (playerX + 1) % maze[0].length;
        } else if (direction == 2) {
            playerY = (playerY + 1) % maze.length;
        } else if (direction == 3) {
            if (playerX == 0) {
                playerX = maze[0].length - 1;
            } else {
                playerX -= 1;
            }
        }
        hasPlayerMoved = true;
    }
}

function moveDown() {
    if (inPrompt) {
        if (cursorUp === true) {
            cursorY += 12;
            cursorUp = false;
        }
        return;
    }
}

function interact() {
    if (inPrompt) {
        if (cursorUp === true) {
            switch(currentEvent) {
                case "DN":
                    dialog("You move deeper into the dungeon");
                    inPrompt = false;
                    defaultScene.scene.start("LevelChangeScene", { change: 1 });
                    break;
                case "UP":
                    dialog("You retreat back to the surface");
                    inPrompt = false;
                    defaultScene.scene.start("LevelChangeScene", { change: -1 });
                    break;
            }
        } else {
            // chose no
            inPrompt = false;
            cursorY = 50;
            cursorUp = true;
        }
        return;
    }
    // hex for current tileCode
    hex = maze[playerY][playerX];
    // check for doors
    bits = parseInt(hex, 16).toString(2).padStart(8, '0');
    bits = bits.split(""); // convert to array
    // rotate array to the right 2 * direction
    bits.unshift(...bits.splice(-2 * direction));
    if (bits[6] === "1") {
        // door in front of us
        canMove = true;
        defaultScene.sound.play("wiz2door");
        moveUp();
        return;
    }
}

function doEvent(eventCode) {
    //this.scene.launch('PromptScene', { message: "test\ntest" });
    //this.scene.pause();
    // stairs n stuff
    switch(eventCode) {
        case "EX":
            defaultScene.scene.stop("MainScene");
            defaultScene.scene.start("EndScene", { music: bgmusic });
            resetPlayer();
            break;
        case "DN":
            
            dialog("Go down the stairs?");
            inPrompt = true;
            currentEvent = eventCode;
            /*
            if (dialogChoice === true) {
                dialog("You move deeper into the dungeon");
                defaultScene.scene.start("LevelChangeScene", { change: 1 });
            }
            */
            break;
        case "UP":
            
            dialog("Go up the stairs?");
            inPrompt = true;
            currentEvent = eventCode;
            //defaultScene.scene.start("LevelChangeScene", { change: -1 });
            break;
        case "CM":
            if (character.compass === false) {
                dialog("You found a Compass");
                character.compass = true;
            }
            break;
        case "GP":
            if (character.gps === false) {
                dialog("You found a Jeweled Amulet");
                character.gps = true;
            }
            break;
        case "M0":
            dialog("You cannot leave");
            break;
        case "M1":
            dialog("Return of Werdna is the best Wizardry");
            break;
        case "M2":
            dialog("There are 2 useful items on this floor");
            break;
        case "M3":
            //dialog("");
            break;
        }
}

function warpPlayer(warpNumber) {
    switch(warpNumber) {
        case "0":
            playerY = 15;
            playerX = 15;
            break;
        case "1":
            break;
        case "2":
            break;
        case "3":
            break;
        case "4":
            break;
        case "5":
            break;
        case "6":
            break;
        case "7":
            break;
        case "8":
            break;
        case "9":
            break;
        case "S":
            // spinner tile
            break;
    }
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
    initialTime += 1; // add one second
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

function dialog(msg) {
    inDialog = true;
    defaultScene.scene.launch('DialogScene', { message: msg });
    defaultScene.scene.pause();
}

function getAdjacentTiles(row, col) {
    var adjLeftRow;
    var adjRightRow;
    var adjLeftCol;
    var adjRightCol;
    if (direction == 0) {
        // facing north
        if (col > 0) {
            adjLeftCol = col - 1;
            adjRightCol = (col + 1) % maze[0].length;
        } else {
            adjLeftCol = maze[0].length - 1;
            adjRightCol = (col + 1) % maze[0].length;
        }
        adjLeftRow = row;
        adjRightRow = row;
    } else if (direction == 1) {
        // facing east
        if (row > 0) {
            adjLeftRow = row - 1;
            adjRightRow = (row + 1) % maze.length;
        } else {
            adjLeftRow = maze.length -1;
            adjRightRow = (row + 1) % maze.length;
        }
        adjLeftCol = col;
        adjRightCol = col;
    } else if (direction == 2) {
        // facing south
        if (col > 0) {
            adjRightCol = col - 1;
            adjLeftCol = (col + 1) % maze[0].length;
        } else {
            adjRightCol = maze[0].length - 1;
            adjLeftCol = (col + 1) % maze[0].length;
        }
        adjLeftRow = row;
        adjRightRow = row;
    } else {
        // facing west
        if (row > 0) {
            adjRightRow = row - 1;
            adjLeftRow = (row + 1) % maze.length;
        } else {
            adjRightRow = maze.length -1;
            adjLeftRow = (row + 1) % maze.length;
        }
        adjLeftCol = col;
        adjRightCol = col;
    }
    //console.log("LEFT:" + adjLeftRow + "," + adjLeftCol + ". RIGHT: " + adjRightRow + "," + adjRightCol);
    return [adjLeftRow, adjLeftCol, adjRightRow, adjRightCol];
}

function processTile(tileCode, far, adjacent, left) {
    var prefix = "";
    if (far === true) {
        prefix += "far_";
    } else {
        prefix += "close_";
    }
    if (adjacent === true) {
        prefix += "adjacent_";
    }
    /*
    N wall  0000 0001   bit 7
    E wall  0000 0100   bit 5
    S wall  0001 0000   bit 3
    W wall  0100 0000   bit 1
    N door  0000 0010   bit 6
    E door  0000 1000   bit 4
    S door  0010 0000   bit 2
    W door  1000 0000   bit 0
    */
    // facingWallIndex = 7 - (direction * 2);
    // facingDoorIndex = 6 - (direction * 2);
    bits = parseInt(tileCode, 16).toString(2).padStart(8, '0');
    bits = bits.split(""); // convert to array
    // rotate array to the right 2 * direction
    bits.unshift(...bits.splice(-2 * direction));
    if (far === false && adjacent === false) { canMove = true; };
    // facing a wall?
    if (bits[7] === "1") {
        // can we walk forward?
        if (far === false && adjacent === false) { canMove = false; };
        if (adjacent === true) {
            if (left === true) {
                defaultScene.add.image(0, 0, prefix + "leftWall").setOrigin(0,0).setDisplaySize(config.width,config.height);
                //console.log("tile=" + tileCode + " direction=" + direction + " bits=" + bits);
            } else {
                // to the right
                defaultScene.add.image(0, 0, prefix + "rightWall").setOrigin(0,0).setDisplaySize(config.width,config.height);
            }
        } else {
            defaultScene.add.image(0, 0, prefix + "centerWall").setOrigin(0,0).setDisplaySize(config.width,config.height);
        }
    }
    // facing a door?
    if (bits[6] === "1") {
        // can we walk forward?
        if (far === false && adjacent === false) { canMove = false; };
        if (adjacent === true) {
            if (left === true) {
                defaultScene.add.image(0, 0, prefix + "leftDoor").setOrigin(0,0).setDisplaySize(config.width,config.height);
                if (bits[7] === "1") { defaultScene.add.image(0, 0, prefix + "leftWall").setOrigin(0,0).setDisplaySize(config.width,config.height); }
            } else {
                // to the right
                defaultScene.add.image(0, 0, prefix + "rightDoor").setOrigin(0,0).setDisplaySize(config.width,config.height);
                if (bits[7] === "1") { defaultScene.add.image(0, 0, prefix + "rightWall").setOrigin(0,0).setDisplaySize(config.width,config.height); }
            }
        } else {
            defaultScene.add.image(0, 0, prefix + "centerDoor").setOrigin(0,0).setDisplaySize(config.width,config.height);
            if (bits[7] === "1") { defaultScene.add.image(0, 0, prefix + "centerWall").setOrigin(0,0).setDisplaySize(config.width,config.height); }
        }
    }
    // door to left?
    if (bits[0] === "1" && adjacent === false) {
        defaultScene.add.image(0, 0, prefix + "leftDoor").setOrigin(0,0).setDisplaySize(config.width,config.height);
    }
    // door to right?
    if (bits[4] === "1" && adjacent === false) {
        defaultScene.add.image(0, 0, prefix + "rightDoor").setOrigin(0,0).setDisplaySize(config.width,config.height);
    }
    // wall to left?
    if (bits[1] === "1" && adjacent === false) {
        defaultScene.add.image(0, 0, prefix + "leftWall").setOrigin(0,0).setDisplaySize(config.width,config.height);
    }
    // wall to right?
    if (bits[5] === "1" && adjacent === false) {
        defaultScene.add.image(0, 0, prefix + "rightWall").setOrigin(0,0).setDisplaySize(config.width,config.height);
    }
}