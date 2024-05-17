class LevelChangeScene extends Phaser.Scene {
    constructor() {
        super({
            key: "LevelChangeScene"
        });
    }
    init(data) {
        levelChange = data.change;
    }
    preload() {
    }
    create() {
    }
    update() {
        if (game.scene.isActive("DialogScene") === false) {
            // only when dialog closed continue, dialog and main run simultaneously during popup
            game.scene.stop("LevelChangeScene");
            character.level += levelChange;
            game.scene.start("MainScene", { level: character.level });
        }
    }
}