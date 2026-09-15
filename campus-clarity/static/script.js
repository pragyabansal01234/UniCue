document.addEventListener("DOMContentLoaded", () => {

    const $ = (selector, scope = document) =>
        scope.querySelector(selector);

    const $$ = (selector, scope = document) =>
        [...scope.querySelectorAll(selector)];


    /* =====================================================
       THEME
    ===================================================== */

    const themeToggle = $("#themeToggle");
    const themeIcon = $("#themeIcon");

    const savedTheme =
        localStorage.getItem("clarity-theme");


    if (savedTheme === "dark") {
        document.body.classList.add("dark");
    }

    updateThemeIcon();


    themeToggle?.addEventListener("click", () => {

        document.body.classList.toggle("dark");

        const isDark =
            document.body.classList.contains("dark");

        localStorage.setItem(
            "clarity-theme",
            isDark ? "dark" : "light"
        );

        updateThemeIcon();

    });


    function updateThemeIcon() {

        if (!themeIcon) return;

        themeIcon.textContent =
            document.body.classList.contains("dark")
                ? "☾"
                : "☼";

    }



    /* =====================================================
       REVEAL ANIMATIONS
    ===================================================== */

    $$(".reveal").forEach((element, index) => {

        element.style.animationDelay =
            `${Math.min(index * 0.07, 0.5)}s`;

    });



    /* =====================================================
       ADD MESSAGE PAGE
    ===================================================== */

    const form = $("#messageForm");
    const textarea = $("#messagesInput");
    const indicator = $("#processingIndicator");
    const submitBtn = $("#submitBtn");
    const sampleBtn = $("#loadSampleBtn");

    const charCount = $("#charCount");
    const lineCount = $("#lineCount");


    const sampleMessages = `[CSE Dept Group] Reminder: Data Structures assignment 3 submission deadline is tomorrow, 15th Sept, 11:59 PM.
[Placement Cell] TCS NQT registration closes on 16th Sept, 5 PM. Only 60 seats left.
[Robotics Club] Workshop on Arduino basics — 16th Sept, 3 PM, Seminar Hall 2. Limited to 40 seats.
[CSE Dept Group] IMPORTANT: Guest lecture on AI Ethics has been CANCELLED due to speaker unavailability.
[Sports Committee] Inter-branch cricket trials — 16th Sept, 4 PM, Main Ground.
[Dean's Office] Scholarship form last date to submit is 18th Sept, no extensions this time.
[Cultural Society] Freshers' Night ticket sales open now, limited to first 200 students, 16th Sept 6 PM onwards.`;


    function updateComposerMeta() {

        if (!textarea) return;

        const text = textarea.value;

        const lines =
            text
                .split("\n")
                .filter(line => line.trim()).length;


        if (charCount) {

            charCount.textContent =
                `${text.length.toLocaleString()} characters`;

        }


        if (lineCount) {

            lineCount.textContent =
                `${lines} ${lines === 1 ? "message" : "messages"}`;

        }

    }


    textarea?.addEventListener(
        "input",
        updateComposerMeta
    );


    updateComposerMeta();



    /* =====================================================
       SAMPLE BUTTON
    ===================================================== */

    sampleBtn?.addEventListener("click", () => {

        if (!textarea) return;


        const isSame =
            textarea.value.trim() ===
            sampleMessages.trim();


        if (isSame) {

            textarea.value = "";

            showToast(
                "Sample cleared. Paste your own messages."
            );

        } else {

            textarea.value = sampleMessages;

            showToast(
                "7 sample campus messages loaded."
            );

        }


        textarea.dispatchEvent(
            new Event("input", {
                bubbles: true
            })
        );


        textarea.focus();

    });



    /* =====================================================
       FORM SUBMIT / AI PROCESSING
    ===================================================== */

    form?.addEventListener("submit", event => {

        if (!textarea?.value.trim()) {

            event.preventDefault();

            showToast(
                "Add at least one message before processing."
            );

            return;

        }


        indicator?.classList.add("active");


        if (submitBtn) {

            submitBtn.disabled = true;

            submitBtn.innerHTML = `
                <span class="processing-ring"></span>
                <span>Processing…</span>
            `;

        }

    });



    /* =====================================================
       DASHBOARD STAT COUNTERS
    ===================================================== */

    $$(".stat-num").forEach(element => {

        const target =
            Number(element.dataset.count || 0);

        const duration = 750;

        const start =
            performance.now();


        function tick(now) {

            const progress =
                Math.min(
                    (now - start) / duration,
                    1
                );


            const eased =
                1 - Math.pow(1 - progress, 3);


            element.textContent =
                Math.round(target * eased);


            if (progress < 1) {

                requestAnimationFrame(tick);

            }

        }


        requestAnimationFrame(tick);

    });



    /* =====================================================
       TODAY DATE
    ===================================================== */

    const todayDate = $("#todayDate");


    if (todayDate) {

        const date = new Date();


        todayDate.textContent =
            date.toLocaleDateString(
                "en-IN",
                {
                    day: "numeric",
                    month: "long"
                }
            );

    }



    /* =====================================================
       DASHBOARD SEARCH
    ===================================================== */

    const searchInput =
        $("#messageSearch");

    const filterPills =
        $$(".filter-pill");

    const noResults =
        $("#noSearchResults");

    const sections =
        $$(".dashboard-section");

    const cards =
        $$(".searchable-item");


    let activeFilter = "all";


    function filterCards() {

        const query =
            (searchInput?.value || "")
                .trim()
                .toLowerCase();


        let visibleCount = 0;


        cards.forEach(item => {

            const section =
                item.closest(".dashboard-section");


            const urgency =
                item.dataset.urgency ||
                section?.dataset.section ||
                "";


            const text =
                item.textContent.toLowerCase();


            const matchesFilter =
                activeFilter === "all" ||
                urgency === activeFilter;


            const matchesSearch =
                !query ||
                text.includes(query);


            const visible =
                matchesFilter &&
                matchesSearch;


            item.style.display =
                visible ? "" : "none";


            if (visible) {
                visibleCount++;
            }

        });



        sections.forEach(section => {

            const sectionType =
                section.dataset.section;


            if (
                activeFilter !== "all" &&
                sectionType !== activeFilter &&
                sectionType !== "uncertain"
            ) {

                section.style.display = "none";

            } else {

                section.style.display = "";

            }

        });


        if (noResults) {

            noResults.hidden =
                visibleCount !== 0;

        }

    }


    searchInput?.addEventListener(
        "input",
        filterCards
    );



    /* =====================================================
       FILTER BUTTONS
    ===================================================== */

    filterPills.forEach(pill => {

        pill.addEventListener("click", () => {

            filterPills.forEach(button => {

                button.classList.remove("active");

            });


            pill.classList.add("active");


            activeFilter =
                pill.dataset.filter;


            filterCards();

        });

    });



    /* =====================================================
       KEYBOARD SEARCH
    ===================================================== */

    document.addEventListener(
        "keydown",
        event => {

            const tag =
                document.activeElement?.tagName;


            if (
                event.key === "/" &&
                ![
                    "INPUT",
                    "TEXTAREA",
                    "SELECT"
                ].includes(tag)
            ) {

                event.preventDefault();

                searchInput?.focus();

            }


            if (
                event.key === "Escape" &&
                document.activeElement === searchInput
            ) {

                searchInput.value = "";

                searchInput.blur();

                filterCards();

            }

        }
    );



    /* =====================================================
       DELETE CONFIRMATION
    ===================================================== */

    $$(".delete-confirm-form, .delete-form")
        .forEach(formElement => {

            formElement.addEventListener(
                "submit",
                event => {

                    const confirmed =
                        window.confirm(
                            "Delete this update? This action cannot be undone."
                        );


                    if (!confirmed) {

                        event.preventDefault();

                    }

                }
            );

        });



    /* =====================================================
       EDIT PAGE PRIORITY PREVIEW
    ===================================================== */

    const urgency =
        $("#urgency");

    const priorityPreview =
        $("#priorityPreview");

    const previewDot =
        $("#previewDot");


    function updatePriorityPreview() {

        if (
            !urgency ||
            !priorityPreview ||
            !previewDot
        ) {
            return;
        }


        const labels = {

            now: "Now — act today",

            soon: "Soon — this week",

            later: "Later — worth knowing"

        };


        priorityPreview.textContent =
            labels[urgency.value] ||
            labels.now;


        const colors = {

            now: "#f04d7a",

            soon: "#f3a52e",

            later: "#13b986"

        };


        previewDot.style.background =
            colors[urgency.value] ||
            colors.now;

    }


    urgency?.addEventListener(
        "change",
        updatePriorityPreview
    );


    updatePriorityPreview();



    /* =====================================================
       TOAST
    ===================================================== */

    function showToast(message) {

        const container =
            $("#toastContainer");


        if (!container) return;


        const toast =
            document.createElement("div");


        toast.className = "toast";


        toast.innerHTML = `
            <span>✦</span>
            <span>${escapeHtml(message)}</span>
        `;


        container.appendChild(toast);


        setTimeout(() => {

            toast.style.opacity = "0";

            toast.style.transform =
                "translateY(8px)";

            toast.style.transition =
                ".25s ease";


            setTimeout(
                () => toast.remove(),
                260
            );

        }, 2800);

    }



    /* =====================================================
       HTML ESCAPE
    ===================================================== */

    function escapeHtml(value) {

        return String(value)
            .replace(
                /[&<>"']/g,
                character => ({

                    "&": "&amp;",
                    "<": "&lt;",
                    ">": "&gt;",
                    '"': "&quot;",
                    "'": "&#039;"

                }[character])
            );

    }

});