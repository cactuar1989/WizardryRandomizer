class PromptScene extends Phaser.Scene {
    constructor() {
        super({
            key: "PromptScene"
        });
    }
    preload() {
        this.load.image("box", "static/assets/box.png");
        this.load.image("cursor", "static/assets/cursor.png");
    }
    create(data) {
        dialogMessage = data.message;
        dialogChoice = null;
        sArr = data.message.split("\n"); // split message into separate lines, number of items in array will be used for setting box height
        maxl = 0; // longest string for setting box width
        for(var i in sArr) {
            if (sArr[i].length > maxl) { maxl = sArr[i].length; }
        }
        maxl += 1; // room for cursor
        
        
        
        cursorY = 65;
        cursorTop = true;
        //var c = this.add.image(50, cursorY, "cursor").setScale(2);
        // add listener for pointer click event
        this.input.on('pointerdown', function(event) {
            //message.destroy();
            this.scene.resume('MainScene');
            this.scene.stop();
        }, this);
        // add listener for keyboard press event
        this.input.keyboard.on('keydown-SPACE', function(event) {
            //message.destroy();
            this.scene.resume('MainScene');
            this.scene.stop();
        }, this);
        this.input.on("pointerup", function(event) {
            pointerEndX = event.upX;
            pointerEndY = event.upY;
            // left pointer drag is < 0
            if ((pointerEndY - pointerStartY) < -MIN_SWIPE_DISTANCE) {
                // swipe up
                if (cursorTop === false) {
                    cursorY -= 12;
                    cursorTop = true;
                    dialogChoice = true;
                }
            } else if ((pointerEndY - pointerStartY) > MIN_SWIPE_DISTANCE) {
                // swipe down
                if (cursorTop === true) {
                    cursorY += 12;
                    cursorTop = false;
                    dialogChoice = false;
                }
            }
        }, this);
        this.input.keyboard.on("keydown", function(event) {
            switch(event.code) {
                case "KeyW":
                case "ArrowUp":
                    if (cursorTop === false) {
                        cursorY -= 12;
                        cursorTop = true;
                        dialogChoice = true;
                        dialog("TEST");
                    }
                    break;
                case "KeyS":
                case "ArrowDown":
                    if (cursorTop === true) {
                        cursorY += 12;
                        cursorTop = false;
                        dialogChoice = false;
                    }
                    break;
            }
        }, this);
    }



    update() {
        this.add.displayList.removeAll();
        this.add.image(38, 36, "box").setOrigin(0, 0).setDisplaySize(maxl*12+12, sArr.length*12+18); // set for 12px prstart font
        var message = this.add.text(58, 45, dialogMessage, { font: "12px prstart" });
        this.add.image(50, cursorY, "cursor").setScale(2);
    }
}