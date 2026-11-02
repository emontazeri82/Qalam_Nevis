"use strict";

/* =========================================================
   QALAM NEVIS — RICH TEXT EDITOR
========================================================= */

document.addEventListener("DOMContentLoaded", () => {

    /* =====================================================
       GET EDITOR ELEMENTS
    ===================================================== */

    const editorContainer =
        document.getElementById("text-editor-container");

    const editor =
        document.getElementById("article-editor");

    const hiddenBody =
        document.getElementById("body");

    const toolbar =
        document.getElementById("editor-toolbar");

    const wordCount =
        document.getElementById("word-count");

    const characterCount =
        document.getElementById("character-count");

    const editorStatus =
        document.getElementById("editor-status");

    const textColor =
        document.getElementById("editor-text-color");

    const linkButton =
        document.getElementById("editor-link-button");

    const copyButton =
        document.getElementById("editor-copy-button");

    const pasteButton =
        document.getElementById("editor-paste-button");

    const ltrButton =
    document.getElementById("editor-ltr-button");

    const rtlButton =
        document.getElementById("editor-rtl-button");

    /* =====================================================
       STOP IF EDITOR DOES NOT EXIST
    ===================================================== */

    if (!editorContainer || !editor || !hiddenBody) {
        return;
    }


    /* =====================================================
       LANGUAGE
    ===================================================== */

    const lang = editorContainer.dataset.lang || "en";


    /* =====================================================
       HELPER — STATUS MESSAGE
    ===================================================== */

    function announce(englishMessage, persianMessage) {

        if (!editorStatus) {
            return;
        }

        editorStatus.textContent =
            lang === "fa"
                ? persianMessage
                : englishMessage;
    }


    /* =====================================================
       HELPER — FOCUS EDITOR
    ===================================================== */

    function focusEditor() {
        editor.focus();
    }

    /* =====================================================
   FIND CURRENT TEXT BLOCK
    ===================================================== */

    function getCurrentBlock() {

        const selection =
            window.getSelection();

        if (!selection || selection.rangeCount === 0) {
            return null;
        }

        let node =
            selection.anchorNode;

        if (node.nodeType === Node.TEXT_NODE) {
            node = node.parentElement;
        }

        while (node && node !== editor) {

            if (
                node.matches(
                    "p, div, h2, h3, blockquote, li"
                )
            ) {
                return node;
            }

            node = node.parentElement;
        }

        return editor;
    }

    /* =====================================================
   SET TEXT DIRECTION
    ===================================================== */

    function setTextDirection(direction) {

        const block =
            getCurrentBlock();

        if (!block) {
            return;
        }

        block.setAttribute(
            "dir",
            direction
        );

        updateEditor();
    }


    /* =====================================================
       HELPER — RUN EDITOR COMMAND
    ===================================================== */

    function runCommand(command, value = null) {

        focusEditor();

        document.execCommand(
            command,
            false,
            value
        );

        updateEditor();
    }


    /* =====================================================
       SYNC EDITOR WITH HIDDEN FORM FIELD
    ===================================================== */

    function syncBody() {

        hiddenBody.value =
            editor.innerHTML.trim();
    }


    /* =====================================================
       GET PLAIN TEXT
    ===================================================== */

    function getPlainText() {

        return editor.innerText
            .replace(/\u00A0/g, " ")
            .trim();
    }


    /* =====================================================
       WORD + CHARACTER COUNTER
    ===================================================== */

    function updateCounts() {

        const text = getPlainText();

        const words =
            text === ""
                ? 0
                : text
                    .split(/\s+/)
                    .filter(Boolean)
                    .length;

        const characters =
            text.length;


        /* Persian */

        if (lang === "fa") {

            if (wordCount) {
                wordCount.textContent =
                    `${words.toLocaleString("fa-IR")} کلمه`;
            }

            if (characterCount) {
                characterCount.textContent =
                    `${characters.toLocaleString("fa-IR")} نویسه`;
            }

            return;
        }


        /* English */

        if (wordCount) {

            wordCount.textContent =
                `${words} ${words === 1 ? "word" : "words"}`;
        }

        if (characterCount) {

            characterCount.textContent =
                `${characters} ${
                    characters === 1
                        ? "character"
                        : "characters"
                }`;
        }
    }


    /* =====================================================
       UPDATE EVERYTHING
    ===================================================== */

    function updateEditor() {

        syncBody();
        updateCounts();
    }


    /* =====================================================
       PLACEHOLDER SUPPORT
    ===================================================== */

    function updateEmptyState() {

        const text =
            editor.innerText.trim();

        const html =
            editor.innerHTML
                .replace(/<br\s*\/?>/gi, "")
                .replace(/&nbsp;/gi, "")
                .trim();

        if (text === "" && html === "") {
            editor.classList.add("is-empty");
        } else {
            editor.classList.remove("is-empty");
        }
    }


    /* =====================================================
       NORMAL TOOLBAR COMMANDS
    ===================================================== */

    if (toolbar) {

        toolbar.addEventListener("mousedown", (event) => {

            /*
             Prevent toolbar buttons from stealing
             the current text selection.
            */

            const button =
                event.target.closest("[data-command]");

            if (button) {
                event.preventDefault();
            }
        });


        toolbar.addEventListener("click", (event) => {

            const button =
                event.target.closest("[data-command]");

            if (!button) {
                return;
            }


            const command =
                button.dataset.command;

            const value =
                button.dataset.value || null;


            /* ---------------------------------------------
               HEADINGS / PARAGRAPH
            --------------------------------------------- */

            if (command === "heading") {

                const block =
                    value || "p";

                runCommand(
                    "formatBlock",
                    block
                );

                return;
            }


            /* ---------------------------------------------
               BLOCKQUOTE
            --------------------------------------------- */

            if (command === "blockquote") {

                runCommand(
                    "formatBlock",
                    "blockquote"
                );

                return;
            }


            /* ---------------------------------------------
               LINK IS HANDLED SEPARATELY
            --------------------------------------------- */

            if (command === "createLink") {
                return;
            }


            /* ---------------------------------------------
               EVERYTHING ELSE
            --------------------------------------------- */

            runCommand(
                command,
                value
            );
        });
    }

    /* =====================================================
   LEFT TO RIGHT
    ===================================================== */

    if (ltrButton) {

        ltrButton.addEventListener(
            "mousedown",
            (event) => {
                event.preventDefault();
            }
        );

        ltrButton.addEventListener(
            "click",
            () => {
                setTextDirection("ltr");
            }
        );
    }
    /* =====================================================
   RIGHT TO LEFT
    ===================================================== */

    if (rtlButton) {

        rtlButton.addEventListener(
            "mousedown",
            (event) => {
                event.preventDefault();
            }
        );

        rtlButton.addEventListener(
            "click",
            () => {
                setTextDirection("rtl");
            }
        );
    }
    /* =====================================================
       TEXT COLOR
    ===================================================== */

    if (textColor) {

        textColor.addEventListener("input", () => {

            runCommand(
                "foreColor",
                textColor.value
            );

            announce(
                "Text color changed.",
                "رنگ متن تغییر کرد."
            );
        });
    }


    /* =====================================================
       CREATE LINK
    ===================================================== */

    if (linkButton) {

        linkButton.addEventListener("mousedown", (event) => {
            event.preventDefault();
        });


        linkButton.addEventListener("click", () => {

            const selection =
                window.getSelection();

            if (
                !selection ||
                selection.rangeCount === 0 ||
                selection.isCollapsed
            ) {

                announce(
                    "Select some text before adding a link.",
                    "برای افزودن پیوند ابتدا بخشی از متن را انتخاب کنید."
                );

                return;
            }


            let url = window.prompt(
                lang === "fa"
                    ? "نشانی پیوند را وارد کنید:"
                    : "Enter the link URL:"
            );


            if (!url) {
                return;
            }


            url = url.trim();


            /*
             If the writer enters:
             example.com

             turn it into:
             https://example.com
            */

            if (
                !/^https?:\/\//i.test(url) &&
                !/^mailto:/i.test(url)
            ) {

                url = `https://${url}`;
            }


            runCommand(
                "createLink",
                url
            );


            /*
             Make generated links safer.
            */

            const links =
                editor.querySelectorAll("a");

            links.forEach((link) => {

                link.setAttribute(
                    "target",
                    "_blank"
                );

                link.setAttribute(
                    "rel",
                    "noopener noreferrer"
                );
            });


            updateEditor();


            announce(
                "Link added.",
                "پیوند افزوده شد."
            );
        });
    }


    /* =====================================================
       COPY
    ===================================================== */

    if (copyButton) {

        copyButton.addEventListener("mousedown", (event) => {
            event.preventDefault();
        });


        copyButton.addEventListener("click", async () => {

            const selection =
                window.getSelection();

            if (
                !selection ||
                selection.rangeCount === 0 ||
                selection.isCollapsed
            ) {

                announce(
                    "Select text to copy.",
                    "متنی را برای کپی انتخاب کنید."
                );

                return;
            }


            const selectedText =
                selection.toString();


            try {

                await navigator.clipboard.writeText(
                    selectedText
                );

                announce(
                    "Text copied.",
                    "متن کپی شد."
                );

            } catch (error) {

                /*
                 Fallback for browsers where
                 Clipboard API isn't available.
                */

                try {

                    document.execCommand("copy");

                    announce(
                        "Text copied.",
                        "متن کپی شد."
                    );

                } catch (fallbackError) {

                    console.error(
                        "Copy failed:",
                        fallbackError
                    );

                    announce(
                        "Copy was blocked by the browser.",
                        "مرورگر اجازه کپی را نداد."
                    );
                }
            }
        });
    }


    /* =====================================================
       PASTE
    ===================================================== */

    if (pasteButton) {

        pasteButton.addEventListener("mousedown", (event) => {
            event.preventDefault();
        });


        pasteButton.addEventListener("click", async () => {

            try {

                const clipboardText =
                    await navigator.clipboard.readText();


                if (!clipboardText) {
                    return;
                }


                focusEditor();


                document.execCommand(
                    "insertText",
                    false,
                    clipboardText
                );


                updateEditor();


                announce(
                    "Text pasted.",
                    "متن جای‌گذاری شد."
                );

            } catch (error) {

                console.warn(
                    "Paste permission denied:",
                    error
                );


                announce(
                    "Use Command + V to paste.",
                    "برای جای‌گذاری از Command + V استفاده کنید."
                );
            }
        });
    }


    /* =====================================================
       PASTE CLEAN TEXT FROM KEYBOARD

       This prevents Word / websites from pasting
       large amounts of unwanted HTML and styles.
    ===================================================== */

    editor.addEventListener("paste", (event) => {

        event.preventDefault();


        const clipboardData =
            event.clipboardData;

        if (!clipboardData) {
            return;
        }


        const text =
            clipboardData.getData("text/plain");


        document.execCommand(
            "insertText",
            false,
            text
        );


        updateEditor();
    });


    /* =====================================================
       INPUT EVENT

       Runs whenever writer types, deletes,
       or modifies content.
    ===================================================== */

    editor.addEventListener("input", () => {

        updateEditor();
        updateEmptyState();
    });


    /* =====================================================
       KEYBOARD SHORTCUTS
    ===================================================== */

    editor.addEventListener("keydown", (event) => {

        const commandKey =
            event.metaKey || event.ctrlKey;


        if (!commandKey) {
            return;
        }


        const key =
            event.key.toLowerCase();


        /* Bold */

        if (key === "b") {

            event.preventDefault();

            runCommand("bold");

            return;
        }


        /* Italic */

        if (key === "i") {

            event.preventDefault();

            runCommand("italic");

            return;
        }


        /* Underline */

        if (key === "u") {

            event.preventDefault();

            runCommand("underline");

            return;
        }
    });


    /* =====================================================
       FORM SUBMISSION

       contenteditable itself is NOT submitted by HTML.

       Before Flask receives the form, copy the editor's
       HTML into:

           <input type="hidden" name="body">

    ===================================================== */

    const form =
        editor.closest("form");


    if (form) {

        form.addEventListener("submit", (event) => {

            updateEditor();


            const plainText =
                getPlainText();


            /*
             The old textarea had "required".

             Since contenteditable doesn't support required
             like an input does, validate it here.
            */

            if (plainText === "") {

                event.preventDefault();

                focusEditor();


                announce(
                    "Please write your article before continuing.",
                    "لطفاً پیش از ادامه متن مقاله را بنویسید."
                );


                window.alert(
                    lang === "fa"
                        ? "لطفاً متن مقاله را وارد کنید."
                        : "Please enter the article body."
                );

                return;
            }


            /*
             Final synchronization before sending
             data to Flask.
            */

            hiddenBody.value =
                editor.innerHTML.trim();
        });
    }


    /* =====================================================
       INITIALIZE EXISTING CONTENT

       This becomes useful later when editing a saved draft.

       Flask can place previously saved HTML in the hidden
       body input and JavaScript loads it into the editor.
    ===================================================== */

    if (
        hiddenBody.value &&
        hiddenBody.value.trim() !== ""
    ) {

        editor.innerHTML =
            hiddenBody.value;
    }


    /* =====================================================
       INITIAL UPDATE
    ===================================================== */
    document.execCommand(
        "defaultParagraphSeparator",
        false,
        "p"
    );

    updateEditor();
    updateEmptyState();

});