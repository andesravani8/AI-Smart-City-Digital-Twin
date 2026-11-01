// ======================================================
// MAIN JAVASCRIPT
// ======================================================

document.addEventListener(
    "DOMContentLoaded",
    function () {

        const mobileMenu =
            document.querySelector(".mobile-menu");

        const sidebar =
            document.querySelector(".sidebar");


        if (mobileMenu && sidebar) {

            mobileMenu.addEventListener(
                "click",
                function () {

                    sidebar.classList.toggle(
                        "open"
                    );

                }
            );

        }


        // Active navigation

        const navItems =
            document.querySelectorAll(
                ".nav-item"
            );


        navItems.forEach(
            function (item) {

                item.addEventListener(
                    "click",
                    function () {

                        navItems.forEach(
                            function (nav) {

                                nav.classList.remove(
                                    "active"
                                );

                            }
                        );

                        item.classList.add(
                            "active"
                        );

                    }
                );

            }
        );

    }
);