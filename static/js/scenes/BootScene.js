class BootScene extends Phaser.Scene {
    constructor() {
        super({
            key: "BootScene"
        });
    }
    preload() {
    }
    create() {
        this.add.text(0, 0, "Preloading font", { font: "1px prstart", fill:"#FFFFFF"});﻿
        this.scene.start("IntroScene");
    }
}