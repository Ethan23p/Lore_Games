## Task List

* PENDING updating prompt_templates - I pasted my latest version of the 'prompt_templates' in prompts.py; it's formatted very awkwardly because I copied it from Logseq, I know it's probably painful how messed up it is, lol. Anyway, please normalize the new template text into the format of the old template json format.

    It's important that you:
        1. use the exact conventions as before;
        2. Definitely don't use HTML style tags (closing tags starting with a slash) because they break your tools. It's an unfortunate bug and it's quite destructive, so again don't even try to use HTML style tags.
        3. don't change the *content* of the writing, but you should fix the formatting and variable mismatches; if you think something should be changed about the writing I'd prefer that you ask me about it before changing it.
        4. There are now two primers for environment, I want to be able to switch between them in the dev environment so please add a simple toggle in the config.