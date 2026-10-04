const USE_SYNTH_VOICE = true; 

// Initial Objects Array using Base64 Data URIs
const LEVEL_1_OBJECTS = [
    { id: 'mary', name: 'Mary (Sweet Bunny)', image: 'data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSI1MCIgaGVpZ2h0PSI1MCI+PHJlY3Qgd2lkdGg9IjUwIiBoZWlnaHQ9IjUwIiBmaWxsPSIjZWVlIi8+PHRleHQgeD0iMjUiIHk9IjMzIiBmb250LXNpemU9IjI1IiB0ZXh0LWFuY2hvcj0ibWlkZGxlIj7wn5C1PC90ZXh0Pjwvc3ZnPg==', x: 300, y: 850, w: 80, h: 120, found: false, soundText: "a sweet little bunny Mary", audioFile: "mary.wav" },
    { id: 'smart', name: 'Smart little bunny', image: 'data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSI1MCIgaGVpZ2h0PSI1MCI+PHJlY3Qgd2lkdGg9IjUwIiBoZWlnaHQ9IjUwIiBmaWxsPSIjZmZlNGI1Ii8+PHRleHQgeD0iMjUiIHk9IjMzIiBmb250LXNpemU9IjI1IiB0ZXh0LWFuY2hvcj0ibWlkZGxlIj7wn5C1PC90ZXh0Pjwvc3ZnPg==', x: 750, y: 620, w: 80, h: 120, found: false, soundText: "a smart little bunny maybe", audioFile: "smart.wav" },
    { id: 'melanie', name: 'Melanie (Cute Bunny)', image: 'data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSI1MCIgaGVpZ2h0PSI1MCI+PHJlY3Qgd2lkdGg9IjUwIiBoZWlnaHQ9IjUwIiBmaWxsPSIjYWRkOGU2Ii8+PHRleHQgeD0iMjUiIHk9IjMzIiBmb250LXNpemU9IjI1IiB0ZXh0LWFuY2hvcj0ibWlkZGxlIj7wn5C1PC90ZXh0Pjwvc3ZnPg==', x: 1200, y: 900, w: 80, h: 120, found: false, soundText: "a cute little bunny Melanie", audioFile: "melanie.wav" },
    { id: 'snuffy', name: 'Snuffy (Grumpy)', image: 'data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSI1MCIgaGVpZ2h0PSI1MCI+PHJlY3Qgd2lkdGg9IjUwIiBoZWlnaHQ9IjUwIiBmaWxsPSIjZmZiNmMxIi8+PHRleHQgeD0iMjUiIHk9IjMzIiBmb250LXNpemU9IjI1IiB0ZXh0LWFuY2hvcj0ibWlkZGxlIj7wn5C1PC90ZXh0Pjwvc3ZnPg==', x: 1650, y: 700, w: 80, h: 120, found: false, soundText: "grumpy Snuffy", audioFile: "snuffy.wav" },
    { id: 'pavilion', name: 'Traditional Pavilion', image: 'data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSI1MCIgaGVpZ2h0PSI1MCI+PHJlY3Qgd2lkdGg9IjUwIiBoZWlnaHQ9IjUwIiBmaWxsPSIjZWVlIi8+PHRleHQgeD0iMjUiIHk9IjMzIiBmb250LXNpemU9IjI1IiB0ZXh0LWFuY2hvcj0ibWlkZGxlIj7im6nvuI88L3RleHQ+PC9zdmc+', x: 250, y: 500, w: 200, h: 150, found: false, soundText: "Traditional Pavilion found", audioFile: "chime1.wav" },
    { id: 'tower', name: 'Tall Observation Tower', image: 'data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSI1MCIgaGVpZ2h0PSI1MCI+PHJlY3Qgd2lkdGg9IjUwIiBoZWlnaHQ9IjUwIiBmaWxsPSIjZWVlIi8+PHRleHQgeD0iMjUiIHk9IjMzIiBmb250LXNpemU9IjI1IiB0ZXh0LWFuY2hvcj0ibWlkZGxlIj7wn5G8PC90ZXh0Pjwvc3ZnPg==', x: 1400, y: 150, w: 100, h: 400, found: false, soundText: "Observation Tower found", audioFile: "chime2.wav" },
    { id: 'kite', name: 'Flying Kite', image: 'data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSI1MCIgaGVpZ2h0PSI1MCI+PHJlY3Qgd2lkdGg9IjUwIiBoZWlnaHQ9IjUwIiBmaWxsPSIjZWVlIi8+PHRleHQgeD0iMjUiIHk9IjMzIiBmb250LXNpemU9IjI1IiB0ZXh0LWFuY2hvcj0ibWlkZGxlIj7wn6SAPC90ZXh0Pjwvc3ZnPg==', x: 1750, y: 250, w: 60, h: 80, found: false, soundText: "Flying Kite found", audioFile: "chime3.wav" },
    { id: 'balloons', name: 'Floating Balloons', image: 'data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSI1MCIgaGVpZ2h0PSI1MCI+PHJlY3Qgd2lkdGg9IjUwIiBoZWlnaHQ9IjUwIiBmaWxsPSIjZWVlIi8+PHRleHQgeD0iMjUiIHk9IjMzIiBmb250LXNpemU9IjI1IiB0ZXh0LWFuY2hvcj0ibWlkZGxlIj7wn46IPC90ZXh0Pjwvc3ZnPg==', x: 450, y: 200, w: 70, h: 90, found: false, soundText: "Floating Balloons found", audioFile: "chime4.wav" }
];

let currentObjects = [];
let currentUserKey = "";
let devMode = false;
let wrongClicks = 0;
let startTime = 0;

const sceneImage = document.getElementById('scene-image');
const sceneWrapper = document.getElementById('scene-wrapper');
const highlightsContainer = document.getElementById('highlights-container');
const sceneItemsContainer = document.getElementById('scene-items-container');
const findList = document.getElementById('find-list');
const counterLabel = document.getElementById('counter');
const wrongCounterLabel = document.getElementById('wrong-counter');
const winScreen = document.getElementById('win-screen');

// Ensures dynamic objects are drawn only after the background image calculates its natural dimensions
sceneImage.addEventListener('load', renderSceneItems);

document.getElementById('login-btn').addEventListener('click', () => {
    const user = document.getElementById('username').value.trim().toLowerCase();
    const pin = document.getElementById('pin').value.trim();
    if (!user || pin.length !== 3 || isNaN(pin)) {
        document.getElementById('login-error').textContent = "Please enter a username and a 3-digit PIN.";
        return;
    }
    currentUserKey = `hiddenFolks_${user}_${pin}`;
    initializeGame();
    document.getElementById('login-screen').classList.remove('active');
});

function initializeGame() {
    startTime = Date.now();
    currentObjects = JSON.parse(JSON.stringify(LEVEL_1_OBJECTS));
    
    const savedState = localStorage.getItem(currentUserKey);
    if (savedState) {
        const parsedState = JSON.parse(savedState);
        currentObjects.forEach(obj => {
            const savedItem = parsedState.find(s => s.id === obj.id);
            if (savedItem && savedItem.found) {
                obj.found = true;
            }
        });
    }

    const savedStats = localStorage.getItem(currentUserKey + "_stats");
    wrongClicks = savedStats ? parseInt(savedStats) : 0;
    
    renderUI();
    if (sceneImage.complete) renderSceneItems(); // Fire immediately if image is already loaded
}

function saveProgress() {
    localStorage.setItem(currentUserKey, JSON.stringify(currentObjects));
    localStorage.setItem(currentUserKey + "_stats", wrongClicks);
}

document.getElementById('reset-btn').addEventListener('click', () => {
    localStorage.removeItem(currentUserKey);
    localStorage.removeItem(currentUserKey + "_stats");
    winScreen.classList.remove('active');
    initializeGame();
});

function playSound(text, fileName) {
    if (USE_SYNTH_VOICE) {
        window.speechSynthesis.cancel(); 
        window.speechSynthesis.speak(new SpeechSynthesisUtterance(text));
    } else {
        new Audio(`assets/audio/${fileName}`).play().catch(e => console.log("Audio file missing", e));
    }
}

// Dynamically stamps the items onto the game scene background 
function renderSceneItems() {
    sceneItemsContainer.innerHTML = '';
    
    const nw = sceneImage.naturalWidth || 1920;
    const nh = sceneImage.naturalHeight || 1080;

    currentObjects.forEach(obj => {
        const img = document.createElement('img');
        img.src = obj.image;
        img.style.position = 'absolute';
        
        // Uses percentages so the items scale perfectly with the window
        img.style.left = `${(obj.x / nw) * 100}%`;
        img.style.top = `${(obj.y / nh) * 100}%`;
        img.style.width = `${(obj.w / nw) * 100}%`;
        img.style.height = `${(obj.h / nh) * 100}%`;
        img.style.objectFit = 'contain';
        
        // Dim the item in the scene if it has already been found
        if (obj.found) {
            img.style.opacity = '0.3';
        }
        
        sceneItemsContainer.appendChild(img);
    });
}

function renderUI() {
    findList.innerHTML = '';
    let foundCount = 0;
    
    currentObjects.forEach(obj => {
        const li = document.createElement('li');
        const img = document.createElement('img');
        img.src = obj.image; 
        img.alt = obj.name;
        img.classList.add('find-thumb');
        
        const span = document.createElement('span');
        span.textContent = obj.name;
        
        li.appendChild(img);
        li.appendChild(span);
        
        if (obj.found) {
            li.classList.add('found');
            foundCount++;
        }
        findList.appendChild(li);
    });
    
    counterLabel.textContent = `Found: ${foundCount} of ${currentObjects.length}`;
    wrongCounterLabel.textContent = `Wrong Clicks: ${wrongClicks}`;
    
    if (foundCount === currentObjects.length) {
        const elapsedSeconds = Math.floor((Date.now() - startTime) / 1000);
        document.getElementById('final-stats').textContent = `Time: ${elapsedSeconds}s | Wrong Clicks: ${wrongClicks}`;
        winScreen.classList.add('active'); 
    }
}

function drawHighlightRing(x, y, w, h, cssClass) {
    const ring = document.createElement('div');
    ring.classList.add(cssClass);
    
    const r = sceneImage.getBoundingClientRect();
    const scaleX = r.width / sceneImage.naturalWidth;
    const scaleY = r.height / sceneImage.naturalHeight;
    
    const widthScaled = w * scaleX;
    const heightScaled = h * scaleY;
    const size = Math.max(widthScaled, heightScaled) * 1.5; 
    
    ring.style.width = `${size}px`;
    ring.style.height = `${size}px`;
    
    // Adjusted coordinates because highlights-container is now relative to the inner wrapper
    ring.style.left = `${(x * scaleX) + (widthScaled / 2) - (size / 2)}px`;
    ring.style.top = `${(y * scaleY) + (heightScaled / 2) - (size / 2)}px`;
    
    highlightsContainer.appendChild(ring);
    
    if (cssClass === 'found-ring') {
        setTimeout(() => ring.remove(), 1000);
    } else if (cssClass === 'hint-pulse') {
        setTimeout(() => ring.remove(), 2000);
    }
}

sceneImage.addEventListener('click', (e) => {
    const r = sceneImage.getBoundingClientRect();
    const scaleX = sceneImage.naturalWidth / r.width;
    const scaleY = sceneImage.naturalHeight / r.height;
    
    const sceneX = (e.clientX - r.left) * scaleX;
    const sceneY = (e.clientY - r.top) * scaleY;
    
    if (devMode) {
        console.log(`[DEV] Clicked X: ${Math.round(sceneX)}, Y: ${Math.round(sceneY)}`);
    }

    const hitObj = currentObjects.find(o => 
        !o.found && 
        sceneX >= o.x && sceneX <= o.x + o.w && 
        sceneY >= o.y && sceneY <= o.y + o.h
    );

    if (hitObj) {
        hitObj.found = true;
        drawHighlightRing(hitObj.x, hitObj.y, hitObj.w, hitObj.h, 'found-ring');
        playSound(hitObj.soundText, hitObj.audioFile);
    } else {
        wrongClicks++;
        playSound("buzz", "buzz.wav");
    }
    
    saveProgress();
    renderUI();
    renderSceneItems(); // Updates the opacity of the stamped object in the scene
});

document.getElementById('hint-btn').addEventListener('click', () => {
    const unfound = currentObjects.filter(o => !o.found);
    if (unfound.length > 0) {
        const target = unfound[Math.floor(Math.random() * unfound.length)];
        drawHighlightRing(target.x, target.y, target.w, target.h, 'hint-pulse');
    }
});

document.getElementById('dev-mode-btn').addEventListener('click', () => {
    devMode = !devMode;
    document.getElementById('dev-panel').style.display = devMode ? 'block' : 'none';
    document.querySelectorAll('.hitbox-outline').forEach(el => el.remove());
    
    if (devMode) {
        const r = sceneImage.getBoundingClientRect();
        const scaleX = r.width / sceneImage.naturalWidth;
        const scaleY = r.height / sceneImage.naturalHeight;

        currentObjects.forEach(obj => {
            const div = document.createElement('div');
            div.classList.add('hitbox-outline');
            div.style.left = `${(obj.x * scaleX)}px`;
            div.style.top = `${(obj.y * scaleY)}px`;
            div.style.width = `${obj.w * scaleX}px`;
            div.style.height = `${obj.h * scaleY}px`;
            div.style.borderColor = obj.found ? 'lime' : 'red'; 
            highlightsContainer.appendChild(div);
        });
    }
});