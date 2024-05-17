class IntroScene extends Phaser.Scene {
    constructor() {
        super({
            key: "IntroScene"
        });
    }
    preload() {
        this.load.image("background", "static/assets/background.png");
        this.load.audio("introMusic", "static/assets/music/Wiz1Maze.mp3");
    }
    create() {
        // background
        this.add.image(0, 0, "background").setOrigin(0,0).setDisplaySize(config.width,config.height);
        var intromusic = this.sound.add("introMusic", {volume: 0.75, loop:true});
        intromusic.play();
        var lost = this.add.text(18, 10, 'LOST', { font: "36px prstart" });
        var fadeOut = this.tweens.add({
            targets: [lost, bgmusic],
            paused: true,
            alpha: {
                from: 1,
                to: 0
            },
            volume: 0,
            ease: 'Linear',
            duration: 2000,
            repeat: 0,
            yoyo: false,
            onComplete: function() {
                lost.destroy();
                game.sound.removeAll();
                game.scene.stop("IntroScene");
                game.scene.start("MainScene");
            }
        }, this);
        var mazed = this.add.text(30, 60, 'Mazed and Confused', { font: "20px prstart" });
        var pressKey = this.add.text(30, 90, 'Press any key to continue', { font: "16px prstart" });
        // add listener for pointer click event
        this.input.on('pointerdown', function(event) {
            mazed.destroy();
            pressKey.destroy();
            fadeOut.play();
        }, this);
        // add listener for keyboard press event
        this.input.keyboard.on('keydown', function(event) {
            mazed.destroy();
            pressKey.destroy();
            fadeOut.play();
        }, this);
    }
    update() {
    }
}