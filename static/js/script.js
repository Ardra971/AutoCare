document.addEventListener("DOMContentLoaded", function () {

    /* =====================================================
       ACCOUNT DROPDOWN
    ====================================================== */

    const accountButton =
        document.getElementById("accountMenuButton");

    const accountMenu =
        document.getElementById("accountMenu");

    const accountArrow =
        document.getElementById("accountArrow");


    if (accountButton && accountMenu) {

        accountButton.addEventListener(
            "click",
            function (event) {

                event.preventDefault();
                event.stopPropagation();

                const isOpen =
                    accountMenu.classList.contains("show");

                if (isOpen) {

                    accountMenu.classList.remove("show");

                    accountButton.setAttribute(
                        "aria-expanded",
                        "false"
                    );

                    if (accountArrow) {
                        accountArrow.textContent = "▼";
                    }

                } else {

                    accountMenu.classList.add("show");

                    accountButton.setAttribute(
                        "aria-expanded",
                        "true"
                    );

                    if (accountArrow) {
                        accountArrow.textContent = "▲";
                    }
                }
            }
        );


        /* CLOSE WHEN CLICKING OUTSIDE */

        document.addEventListener(
            "click",
            function (event) {

                if (
                    !accountButton.contains(event.target) &&
                    !accountMenu.contains(event.target)
                ) {

                    accountMenu.classList.remove("show");

                    accountButton.setAttribute(
                        "aria-expanded",
                        "false"
                    );

                    if (accountArrow) {
                        accountArrow.textContent = "▼";
                    }
                }
            }
        );


        /* CLOSE WITH ESCAPE */

        document.addEventListener(
            "keydown",
            function (event) {

                if (event.key === "Escape") {

                    accountMenu.classList.remove("show");

                    accountButton.setAttribute(
                        "aria-expanded",
                        "false"
                    );

                    if (accountArrow) {
                        accountArrow.textContent = "▼";
                    }
                }
            }
        );
    }


    /* =====================================================
       BOOKING SERVICE SELECTION
    ====================================================== */

    const form =
        document.getElementById("booking-form");

    const serviceButtons =
        document.querySelectorAll(".add-service-button");

    const selectedServicesList =
        document.getElementById("selected-services-list");

    const selectedServiceInputs =
        document.getElementById("selected-service-inputs");

    const selectedServiceCount =
        document.getElementById("selected-service-count");

    const summaryServiceCount =
        document.getElementById("summary-service-count");

    const estimatedCost =
        document.getElementById("estimated-cost");

    const bookingDate =
        document.getElementById("booking_date");


    if (
        !selectedServicesList ||
        !selectedServiceInputs ||
        !selectedServiceCount ||
        !estimatedCost
    ) {
        return;
    }


    const selectedServices = new Map();


    if (bookingDate) {

        const today = new Date();

        const localToday = new Date(
            today.getTime() -
            today.getTimezoneOffset() * 60000
        )
        .toISOString()
        .split("T")[0];

        bookingDate.min = localToday;
    }


    function renderSelectedServices() {

        selectedServicesList.innerHTML = "";
        selectedServiceInputs.innerHTML = "";

        if (selectedServices.size === 0) {

            const emptyMessage =
                document.createElement("p");

            emptyMessage.className =
                "no-selected-services";

            emptyMessage.textContent =
                "No services selected.";

            selectedServicesList.appendChild(
                emptyMessage
            );
        }

        let total = 0;


        selectedServices.forEach(
            function (service) {

                total += service.price;

                const selectedService =
                    document.createElement("div");

                selectedService.className =
                    "selected-service-item";


                const serviceInfo =
                    document.createElement("div");

                serviceInfo.className =
                    "selected-service-info";


                const serviceName =
                    document.createElement("strong");

                serviceName.textContent =
                    service.name;


                const servicePrice =
                    document.createElement("span");

                servicePrice.textContent =
                    `₹${service.price.toFixed(2)}`;


                serviceInfo.appendChild(serviceName);
                serviceInfo.appendChild(servicePrice);


                const removeButton =
                    document.createElement("button");

                removeButton.type = "button";

                removeButton.className =
                    "remove-service-button";

                removeButton.textContent =
                    "Remove";


                removeButton.addEventListener(
                    "click",
                    function () {

                        selectedServices.delete(
                            service.id
                        );


                        const originalButton =
                            document.querySelector(
                                `.add-service-button[data-service-id="${service.id}"]`
                            );


                        if (originalButton) {

                            originalButton.textContent =
                                "Add Service";

                            originalButton.classList.remove(
                                "selected"
                            );

                            originalButton.classList.remove(
                                "added"
                            );

                            originalButton.disabled =
                                false;

                            originalButton.setAttribute(
                                "aria-pressed",
                                "false"
                            );
                        }


                        renderSelectedServices();
                    }
                );


                selectedService.appendChild(
                    serviceInfo
                );

                selectedService.appendChild(
                    removeButton
                );

                selectedServicesList.appendChild(
                    selectedService
                );


                const hiddenInput =
                    document.createElement("input");

                hiddenInput.type = "hidden";

                hiddenInput.name = "services";

                hiddenInput.value = service.id;

                selectedServiceInputs.appendChild(
                    hiddenInput
                );
            }
        );


        const count =
            selectedServices.size;

        const countText =
            `${count} service${count === 1 ? "" : "s"}`;

        selectedServiceCount.textContent =
            countText;


        if (summaryServiceCount) {

            summaryServiceCount.textContent =
                countText;
        }


        estimatedCost.textContent =
            total.toFixed(2);
    }


    serviceButtons.forEach(
        function (button) {

            button.addEventListener(
                "click",
                function () {

                    const serviceId =
                        button.dataset.serviceId;

                    const serviceName =
                        button.dataset.serviceName;

                    const servicePrice =
                        Number.parseFloat(
                            button.dataset.servicePrice
                        ) || 0;


                    if (
                        selectedServices.has(
                            serviceId
                        )
                    ) {
                        return;
                    }


                    selectedServices.set(
                        serviceId,
                        {
                            id: serviceId,
                            name: serviceName,
                            price: servicePrice
                        }
                    );


                    button.textContent =
                        "Added";

                    button.classList.add(
                        "selected"
                    );

                    button.classList.add(
                        "added"
                    );

                    button.setAttribute(
                        "aria-pressed",
                        "true"
                    );


                    renderSelectedServices();
                }
            );
        }
    );


    if (form) {

        form.addEventListener(
            "submit",
            function (event) {

                if (
                    selectedServices.size === 0
                ) {

                    event.preventDefault();

                    alert(
                        "Please select at least one service."
                    );

                    return;
                }


                if (
                    bookingDate &&
                    bookingDate.value
                ) {

                    const today =
                        new Date();

                    const localToday =
                        new Date(
                            today.getTime() -
                            today.getTimezoneOffset() *
                            60000
                        )
                        .toISOString()
                        .split("T")[0];


                    if (
                        bookingDate.value <
                        localToday
                    ) {

                        event.preventDefault();

                        alert(
                            "Please select today or a future service date."
                        );

                        return;
                    }
                }
            }
        );
    }


    renderSelectedServices();

});