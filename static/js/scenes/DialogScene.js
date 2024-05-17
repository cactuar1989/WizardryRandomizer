class DialogScene extends Phaser.Scene {
    constructor() {
        super({
            key: "DialogScene"
        });
    }
    preload() {
        this.load.image("box", "static/assets/box.png");
    }
    create(data) {
        var sArr = data.message.split("\n"); // split message into separate lines, number of items in array will be used for setting box height
        var maxl = 0; // longest string for setting box width
        for(var i in sArr) {
            if (sArr[i].length > maxl) { maxl = sArr[i].length; }
        }
        this.add.image(38, 36, "box").setOrigin(0, 0).setDisplaySize(maxl*12+12, sArr.length*12+18); // set for 12px prstart font
        var message = this.add.text(45, 45, data.message, { font: "12px prstart" });
        // add listener for pointer click event
        this.input.on('pointerdown', function(event) {
            message.destroy();
            this.scene.resume('MainScene');
            this.scene.stop();
            inDialog = false;
        }, this);
        // add listener for keyboard press event
        this.input.keyboard.on('keydown-SPACE', function(event) {
            message.destroy();
            this.scene.resume('MainScene');
            this.scene.stop();
            inDialog = false;
        }, this);
    }
    update() {
    }
}