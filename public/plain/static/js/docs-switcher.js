// From document of PicoCSS.
"use strict";
!function() {
    var t = {
        _state: "closed-on-mobile",
        toggleLink: document.getElementById("toggle-docs-navigation"),
        nav: document.querySelector("main > aside > nav"),
        init() {
            this.onToggleClick()
        },
        onToggleClick() {
            this.toggleLink.addEventListener("click", e=>{
                e.preventDefault(),
                "closed-on-mobile" == this.state ? this.state = "open" : this.state = "closed-on-mobile",
                this.nav.removeAttribute("class"),
                this.nav.classList.add(this.state)
            }
            , !1)
        },
        get state() {
            return this._state
        },
        set state(e) {
            this._state = e
        }
    };
    t.init()
}();