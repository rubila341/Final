document.addEventListener("DOMContentLoaded", () => {
    const buttons = {
        prev: document.querySelector(".btn--left"),
        next: document.querySelector(".btn--right"),
    };
    const cardsContainerEl = document.querySelector(".carousel__cards");
    const appBgContainerEl = document.querySelector(".carousel__background");

    buttons.next.addEventListener("click", () => swapCards("right"));
    buttons.prev.addEventListener("click", () => swapCards("left"));

    function swapCards(direction) {
        const currentCardEl = cardsContainerEl.querySelector(".current--card");
        const previousCardEl = cardsContainerEl.querySelector(".previous--card");
        const nextCardEl = cardsContainerEl.querySelector(".next--card");

        const currentBgImageEl = appBgContainerEl.querySelector(".current--image");
        const previousBgImageEl = appBgContainerEl.querySelector(".previous--image");
        const nextBgImageEl = appBgContainerEl.querySelector(".next--image");

        swapCardsClass();
        changeInfo(direction);

        function swapCardsClass() {
            currentCardEl.classList.remove("current--card");
            previousCardEl.classList.remove("previous--card");
            nextCardEl.classList.remove("next--card");

            currentBgImageEl.classList.remove("current--image");
            previousBgImageEl.classList.remove("previous--image");
            nextBgImageEl.classList.remove("next--image");

            currentBgImageEl.style.zIndex = "-2";
            currentCardEl.style.zIndex = "50";

            if (direction === "right") {
                previousCardEl.style.zIndex = "20";
                nextCardEl.style.zIndex = "30";

                nextBgImageEl.style.zIndex = "-1";

                currentCardEl.classList.add("previous--card");
                previousCardEl.classList.add("next--card");
                nextCardEl.classList.add("current--card");

                currentBgImageEl.classList.add("previous--image");
                previousBgImageEl.classList.add("next--image");
                nextBgImageEl.classList.add("current--image");
            } else if (direction === "left") {
                previousCardEl.style.zIndex = "30";
                nextCardEl.style.zIndex = "20";

                previousBgImageEl.style.zIndex = "-1";

                currentCardEl.classList.add("next--card");
                previousCardEl.classList.add("current--card");
                nextCardEl.classList.add("previous--card");

                currentBgImageEl.classList.add("next--image");
                previousBgImageEl.classList.add("current--image");
                nextBgImageEl.classList.add("previous--image");
            }
        }
    }

    function changeInfo(direction) {
        let currentInfoEl = cardInfosContainerEl.querySelector(".current--info");
        let previousInfoEl = cardInfosContainerEl.querySelector(".previous--info");
        let nextInfoEl = cardInfosContainerEl.querySelector(".next--info");

        gsap.timeline()
            .to([buttons.prev, buttons.next], {
                duration: 0.2,
                opacity: 0.5,
                pointerEvents: "none",
            })
            .to(
                currentInfoEl.querySelectorAll(".text"),
                {
                    duration: 0.4,
                    stagger: 0.1,
                    translateY: "-120px",
                    opacity: 0,
                },
                "-="
            )
            .call(() => swapInfosClass(direction))
            .fromTo(
                direction === "right"
                    ? nextInfoEl.querySelectorAll(".text")
                    : previousInfoEl.querySelectorAll(".text"),
                {
                    opacity: 0,
                    translateY: "40px",
                },
                {
                    duration: 0.4,
                    stagger: 0.1,
                    translateY: "0px",
                    opacity: 1,
                }
            )
            .to([buttons.prev, buttons.next], {
                duration: 0.2,
                opacity: 1,
                pointerEvents: "all",
            });

        function swapInfosClass() {
            currentInfoEl.classList.remove("current--info");
            previousInfoEl.classList.remove("previous--info");
            nextInfoEl.classList.remove("next--info");

            if (direction === "right") {
                currentInfoEl.classList.add("previous--info");
                nextInfoEl.classList.add("current--info");
                previousInfoEl.classList.add("next--info");
            } else if (direction === "left") {
                currentInfoEl.classList.add("next--info");
                nextInfoEl.classList.add("previous--info");
                previousInfoEl.classList.add("current--info");
            }
        }
    }
});
