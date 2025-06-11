// DOM 요소들
const categoryButtons = document.querySelectorAll('.category-btn');
const categoryInput = document.getElementById('category');
const dynamicFields = document.getElementById('dynamicFields');
const cafeFields = document.getElementById('cafeFields');
const restaurantFields = document.getElementById('restaurantFields');
const reviewFields = document.getElementById('reviewFields');
const blogForm = document.getElementById('blogForm');
const autocompleteBtn = document.getElementById('autocompleteBtn');
const generateBtn = document.getElementById('generateBtn');
const loadingSpinner = document.getElementById('loadingSpinner');
const resultSection = document.getElementById('resultSection');
const generatedPost = document.getElementById('generatedPost');
const copyBtn = document.getElementById('copyBtn');

// 카테고리 선택 이벤트
categoryButtons.forEach(button => {
    button.addEventListener('click', function() {
        // 모든 버튼에서 active 클래스 제거
        categoryButtons.forEach(btn => btn.classList.remove('active'));
        
        // 클릭된 버튼에 active 클래스 추가
        this.classList.add('active');
        
        // 선택된 카테고리 값 저장
        const selectedCategory = this.dataset.category;
        categoryInput.value = selectedCategory;
        
        // 해당 필드 그룹 표시
        showFieldsForCategory(selectedCategory);
        
        // 동적 필드 영역 표시
        dynamicFields.style.display = 'block';
    });
});

// 카테고리별 필드 표시 함수
function showFieldsForCategory(category) {
    // 모든 필드 그룹 숨기기
    cafeFields.style.display = 'none';
    restaurantFields.style.display = 'none';
    reviewFields.style.display = 'none';
    
    // 선택된 카테고리에 맞는 필드 그룹 표시
    switch(category) {
        case '카페':
            cafeFields.style.display = 'block';
            break;
        case '맛집':
            restaurantFields.style.display = 'block';
            break;
        case '리뷰':
            reviewFields.style.display = 'block';
            break;
    }
}

// 폼 제출 이벤트
blogForm.addEventListener('submit', async function(e) {
    e.preventDefault();
    
    const formData = new FormData(this);
    
    // 로딩 상태 표시
    showLoading(true);
    resultSection.style.display = 'none';
    
    try {
        const response = await fetch('/generate', {
            method: 'POST',
            body: formData
        });
        
        const result = await response.json();
        
        if (result.success) {
            // 성공적으로 생성된 경우
            generatedPost.textContent = result.generated_post;
            resultSection.style.display = 'block';
            
            // 성공 메시지 표시
            showMessage('블로그 포스트가 성공적으로 생성되었습니다!', 'success');
            
            // 스크롤을 결과 영역으로 이동
            resultSection.scrollIntoView({ behavior: 'smooth' });
        } else {
            // 오류 발생
            showMessage('오류가 발생했습니다: ' + result.error, 'error');
        }
    } catch (error) {
        console.error('Error:', error);
        showMessage('네트워크 오류가 발생했습니다. 다시 시도해주세요.', 'error');
    } finally {
        showLoading(false);
    }
});

// 복사 버튼 이벤트
copyBtn.addEventListener('click', function() {
    const text = generatedPost.textContent;
    
    navigator.clipboard.writeText(text).then(() => {
        const originalText = copyBtn.textContent;
        copyBtn.textContent = '✅ 복사됨!';
        copyBtn.style.background = '#48bb78';
        
        setTimeout(() => {
            copyBtn.textContent = originalText;
            copyBtn.style.background = '';
        }, 2000);
    }).catch(err => {
        console.error('복사 실패:', err);
        showMessage('복사에 실패했습니다. 텍스트를 직접 선택해서 복사해주세요.', 'error');
    });
});

// 로딩 상태 표시/숨기기
function showLoading(show) {
    if (show) {
        loadingSpinner.style.display = 'block';
        generateBtn.disabled = true;
        generateBtn.textContent = '🔄 생성 중...';
    } else {
        loadingSpinner.style.display = 'none';
        generateBtn.disabled = false;
        generateBtn.textContent = '🚀 전송 (포스트 생성)';
    }
}

// 메시지 표시 함수
function showMessage(message, type) {
    // 기존 메시지 제거
    const existingMessage = document.querySelector('.success-message, .error-message');
    if (existingMessage) {
        existingMessage.remove();
    }
    
    // 새 메시지 생성
    const messageDiv = document.createElement('div');
    messageDiv.className = type === 'success' ? 'success-message' : 'error-message';
    messageDiv.textContent = message;
    
    // 컨테이너 상단에 추가
    const container = document.querySelector('.container');
    container.insertBefore(messageDiv, container.firstChild);
    
    // 3초 후 자동 제거
    setTimeout(() => {
        messageDiv.remove();
    }, 5000);
    
    // 메시지로 스크롤
    messageDiv.scrollIntoView({ behavior: 'smooth' });
}

// 입력 필드 실시간 유효성 검사
document.addEventListener('DOMContentLoaded', function() {
    const inputs = document.querySelectorAll('input[type="text"], textarea');
    
    inputs.forEach(input => {
        input.addEventListener('input', function() {
            // 입력값이 있으면 테두리 색상 변경
            if (this.value.trim()) {
                this.style.borderColor = '#48bb78';
            } else {
                this.style.borderColor = '#e2e8f0';
            }
        });
    });
});

// 키보드 단축키
document.addEventListener('keydown', function(e) {
    // Ctrl+Enter로 폼 제출
    if (e.ctrlKey && e.key === 'Enter') {
        e.preventDefault();
        if (categoryInput.value) {
            blogForm.dispatchEvent(new Event('submit'));
        }
    }
    
    // Esc키로 결과 영역 닫기
    if (e.key === 'Escape') {
        resultSection.style.display = 'none';
    }
});

// 페이지 로드 시 초기화
document.addEventListener('DOMContentLoaded', function() {
    console.log('블로그 포스팅 자동생성기가 준비되었습니다!');
    
    // 첫 번째 카테고리 버튼에 포커스
    if (categoryButtons.length > 0) {
        categoryButtons[0].focus();
    }
});

// -------------------------------------------------------------------
// 실시간 자동완성 로직
// -------------------------------------------------------------------
const detailsTextarea = document.getElementById('details');
const suggestionOverlay = document.getElementById('suggestion-overlay');
let currentSuggestion = '';
let debounceTimer;
let isAutocompleteEnabled = false; // 자동완성 기능 활성화 상태, 초기값은 false

// 자동완성 ON/OFF 토글 버튼 이벤트 리스너
autocompleteBtn.addEventListener('click', () => {
    isAutocompleteEnabled = !isAutocompleteEnabled; // 상태를 반전시킴
    autocompleteBtn.classList.toggle('active'); // 'active' 클래스를 토글

    if (isAutocompleteEnabled) {
        autocompleteBtn.innerHTML = '✨ 자동완성 ON';
    } else {
        autocompleteBtn.innerHTML = '✨ 자동완성 OFF';
        suggestionOverlay.innerText = ''; // 기능을 끄면 보이는 추천 단어 지우기
        currentSuggestion = '';
    }
});

// 텍스트를 입력할 때 API 호출 (디바운싱 적용)
detailsTextarea.addEventListener('input', () => {
    if (!isAutocompleteEnabled) return; // 기능이 꺼져있으면 여기서 중단

    clearTimeout(debounceTimer);
    const prompt = detailsTextarea.value;

    if (prompt.trim().length === 0) {
        suggestionOverlay.innerText = '';
        currentSuggestion = '';
        return;
    }

    debounceTimer = setTimeout(() => {
        fetchAutocomplete(prompt);
    }, 300); // 300ms 디바운스
});

// Tab 키를 눌렀을 때 자동완성 적용
detailsTextarea.addEventListener('keydown', (e) => {
    // 기능이 켜져 있고, 추천 단어가 있을 때만 Tab으로 완성
    if (isAutocompleteEnabled && e.key === 'Tab' && currentSuggestion) {
        e.preventDefault(); // 기본 Tab 동작(포커스 이동) 방지
        detailsTextarea.value += currentSuggestion;
        suggestionOverlay.innerText = '';
        currentSuggestion = '';
    }
});

// 텍스트 영역을 벗어나면 추천 내용 지우기
detailsTextarea.addEventListener('blur', () => {
    suggestionOverlay.innerText = '';
    currentSuggestion = '';
});

// 자동완성 API 호출 함수
async function fetchAutocomplete(prompt) {
    try {
        const response = await fetch('/text_autocomplete', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ prompt: prompt })
        });
        const result = await response.json();

        if (result.success && result.suggestion) {
            // 현재 텍스트와 추천 텍스트가 겹치지 않게 표시
            const pre = ' '.repeat(prompt.length);
            suggestionOverlay.innerText = pre + result.suggestion;
            currentSuggestion = result.suggestion;
        } else {
            suggestionOverlay.innerText = '';
            currentSuggestion = '';
        }
    } catch (error) {
        console.error('Autocomplete error:', error);
        suggestionOverlay.innerText = '';
        currentSuggestion = '';
    }
} 