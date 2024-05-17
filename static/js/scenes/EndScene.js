class EndScene extends Phaser.Scene {
    constructor() {
        super({
            key: "EndScene"
        });
    }
    init(data) {
        //console.log(data);
        bgmusic = data.music;
    }
    preload() {
        this.load.image('background', 'static/assets/background.png');
    }
    create() {
        // background
        var bg = this.add.image(0, 0, 'background').setOrigin(0,0).setDisplaySize(config.width,config.height);
        var exit = this.add.text(18, 10, 'EXIT', { font: "36px prstart" });
        var fadeOut = this.tweens.add({
            targets: [exit, bg],
            paused: true,
            alpha: {
                from: 1,
                to: 0
            },
            ease: 'Linear',
            duration: 1000,
            repeat: 0,
            yoyo: false,
            onComplete: function() {
                exit.destroy();
                game.scene.stop("EndScene");
                bgmusic = null;
                game.scene.start("IntroScene");
            }
        }, this);
        var pressKey = this.add.text(30, 90, 'Press any key to play again', { font: "16px prstart" });
        // add listener for pointer click event
        this.input.on('pointerdown', function(event) {
            data.bgmusic.stop();
            pressKey.destroy();
            fadeOut.play();
        }, this);
        // add listener for keyboard press event
        this.input.keyboard.on('keydown', function(event) {
            bgmusic.stop();
            pressKey.destroy();
            fadeOut.play();
        }, this);
    }
    update() {
    }
}