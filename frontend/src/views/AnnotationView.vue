<template>
  <div class="post-annotation-tool">
    <!-- Card for LLM Outputs -->
    <el-card shadow="hover" class="llm-card">
      <h2 class="main-heading">Template Title</h2>

      <!-- Progress Bar Section-->
      <div class="progress-section">
        <div class="model-name">
          <strong>{{ modelName }} Outputs</strong>
        </div>
        <el-progress
          :percentage="progressPercentage"
          :text-inside="true"
          :stroke-width="20"
          status="active"
          class="progress-bar"
        >
          <template #default>
            <span class="progress-text">
              {{ currentProgress }} / {{ totalOutputs }}
            </span>
          </template>
        </el-progress>
      </div>

      <!-- Text Compare Section -->
      <div class="text-compare-section">
        <el-row :gutter="20">
          <el-col :xs="24" :sm="12" class="text-col">
            <h3>Text A</h3>
            <el-input
              type="textarea"
              v-model="textData.textA"
              rows="6"
              readonly
            />
          </el-col>
          <el-col :xs="24" :sm="12" class="text-col">
            <h3>Text B</h3>
            <el-input
              type="textarea"
              v-model="textData.textB"
              rows="6"
              readonly
            />
          </el-col>
        </el-row>
      </div>

      <!-- Rating Section -->
      <div class="rating-section">
        <span>Similarity Score:</span>
        <el-radio-group v-model="similarityScore" class="score-group">
          <el-radio-button v-for="score in 5" :key="score" :label="score">
            {{ score }}
          </el-radio-button>
        </el-radio-group>
      </div>

      <!-- Action Buttons -->
      <el-row type="flex" justify="center" class="action-row">
        <el-button
          class="action-button"
          type="info"
          @click="selectTask"
          size="large"
        >
          Select Task
        </el-button>
        <el-button
          class="action-button"
          type="warning"
          @click="changeTask"
          size="large"
        >
          Change
        </el-button>
        <el-button
          class="action-button"
          type="primary"
          @click="submitAnnotations"
          size="large"
        >
          Submit
        </el-button>
      </el-row>
    </el-card>

    <!-- Annotation Guidelines Section -->
    <el-card class="annotation-guidelines-card" shadow="hover">
      <h2 class="main-heading">Annotation Guidelines</h2>

      <!-- Table of Contents -->
      <div class="table-of-contents">
        <h3>Contents</h3>
        <ul>
          <li>
            <a href="#annotation-instructions">Annotation Instructions</a>
          </li>
          <li>
            <a href="#example-table">Example Table</a>
          </li>
        </ul>
      </div>

      <div class="guidelines-content">
        <!-- Annotation Instructions -->
        <h3 id="annotation-instructions">Annotation Instructions</h3>
        <ol class="instructions-list">
          <li>
            <strong>Step One:</strong>
            <p>Review the texts on the left and right.</p>
          </li>
          <li>
            <strong>Step Two:</strong>
            <p>Assign a similarity score from 1 to 5.</p>
          </li>
          <li>
            <strong>Step Three:</strong>
            <p>Submit your annotation by clicking <em>Submit</em>.</p>
          </li>
        </ol>

        <!-- Example Table -->
        <h3 id="example-table">Example Table</h3>
        <el-table
          :data="tableData"
          border
          style="width: 100%"
          class="instruction-table"
        >
          <el-table-column prop="columnA" label="Column A" width="120" />
          <el-table-column prop="columnB" label="Column B" />
        </el-table>
      </div>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, watch } from "vue";
import { useStore } from "vuex";
import { ElMessage } from "element-plus";
import {
  fetchNextAnnotationData,
  submitAnnotation,
  getAnnotationProgress,
  IAnnotationData,
} from "@/api/annotation";

const store = useStore();
const userName = computed(() => store.state.user.username);

// Text data
const textData = ref<IAnnotationData>({
  id: 0,
  textA: "",
  textB: "",
});

// Progress related
const currentProgress = ref(0);
const totalOutputs = ref(0);
const progressPercentage = computed(() => {
  return totalOutputs.value === 0
    ? 0
    : ((currentProgress.value / totalOutputs.value) * 100).toFixed(2);
});

// Similarity score
const similarityScore = ref(0);

// Load next data
async function loadNextData() {
  if (!userName.value) {
    ElMessage.warning("Please enter your username first");
    return;
  }

  try {
    const data = await fetchNextAnnotationData(userName.value);
    if (data) {
      textData.value = data;
      similarityScore.value = 0; // 重置评分
    } else {
      ElMessage.success("You have completed all annotations!");
    }
  } catch (error) {
    ElMessage.error("Failed to load next annotation");
  }
}

// Update progress
async function updateProgress() {
  if (!userName.value) return;

  try {
    const progress = await getAnnotationProgress(userName.value);
    currentProgress.value = progress.completed;
    totalOutputs.value = progress.total;
  } catch (error) {
    ElMessage.error("Failed to fetch progress");
  }
}

// Submit annotation
async function submitAnnotations() {
  if (!userName.value) {
    ElMessage.warning("Please enter your username first");
    return;
  }

  if (similarityScore.value === 0) {
    ElMessage.warning("Please select a similarity score");
    return;
  }

  try {
    await submitAnnotation({
      dataId: textData.value.id,
      userName: userName.value,
      score: similarityScore.value,
    });
    ElMessage.success("Annotation submitted successfully!");
    await updateProgress();
    await loadNextData();
  } catch (error) {
    ElMessage.error("Failed to submit annotation");
  }
}

// Listen to username change
watch(userName, async (newUserName) => {
  if (newUserName) {
    await updateProgress();
    await loadNextData();
  }
});

onMounted(async () => {
  if (userName.value) {
    await updateProgress();
    await loadNextData();
  }
});

// Modify selectTask and changeTask functions
function selectTask() {
  loadNextData();
}

function changeTask() {
  loadNextData();
}

// Add missing reactive properties
const modelName = ref("GPT-4"); // Or other model name
const tableData = ref([
  {
    columnA: "Example 1",
    columnB: "Description for example 1",
  },
  {
    columnA: "Example 2",
    columnB: "Description for example 2",
  },
]);
</script>

<style scoped>
.post-annotation-tool {
  padding: 20px;
  max-width: 1000px;
  margin: 0 auto;
  background-color: #ffffff;
}

.llm-card {
  margin-bottom: 10px;
  padding: 0px;
}

.llm-card h2 {
  margin-top: 2px;
}

.main-heading {
  text-align: center;
  margin-bottom: 10px;
}

/* Progress Bar Section */
.progress-section {
  text-align: center;
  margin-bottom: 20px;
}
.model-name {
  font-size: 18px;
  color: #606266;
  margin-bottom: 10px;
}
.model-name strong {
  font-weight: bold;
  color: #303133;
}
.progress-bar {
  display: inline-block;
  width: 80%;
}
.progress-text {
  font-size: 16px;
  color: #ffffff;
}
.el-progress-bar__inner {
  background-color: #409eff;
}

/* Text Compare Section */
.text-compare-section {
  margin-bottom: 20px;
}
.text-col {
  margin-bottom: 20px;
}

/* Rating Section */
.rating-section {
  margin-bottom: 20px;
  text-align: center;
  font-size: 16px;
}

/* Action Buttons */
.action-row {
  width: 100%;
  display: flex;
  justify-content: center;
  margin-bottom: 0px;
}
.action-button {
  font-size: 16px;
  padding: 12px 24px;
  margin-right: 20px;
  width: 200px;
}
.action-row .el-button:last-child {
  margin-right: 0;
}

/* Annotation Guidelines Section */
.annotation-guidelines-card {
  margin-top: 20px;
}
.annotation-guidelines-card h2 {
  margin-top: 2px;
}
.guidelines-content h3 {
  margin-top: 20px;
  color: #333;
}
.guidelines-content p {
  font-size: 14px;
  line-height: 1.6;
  color: #666;
}
.instructions-list,
.instructions-list ul {
  font-size: 14px;
  line-height: 1.6;
  color: #666;
}
.instructions-list li,
.instructions-list ul li {
  margin-bottom: 10px;
}
.instructions-list strong {
  font-weight: bold;
}
.instructions-list em {
  font-style: italic;
  color: #555;
}
.instruction-table .el-table th {
  background-color: #f5f7fa;
  font-weight: bold;
}

/* Styles for the Table of Contents */
.table-of-contents {
  margin-bottom: 20px;
}
.table-of-contents h3 {
  margin-bottom: 10px;
}
.table-of-contents ul {
  list-style-type: none;
  padding-left: 0;
}
.table-of-contents li {
  margin-bottom: 5px;
}
.table-of-contents a {
  color: #409eff;
  text-decoration: none;
}
.table-of-contents a:hover {
  text-decoration: underline;
}

/* Responsive Design */
@media (max-width: 768px) {
  .action-row {
    flex-wrap: wrap;
  }
  .action-button {
    margin-bottom: 10px;
    width: 100%;
    margin-right: 0;
  }
  .action-row .el-button:last-child {
    margin-bottom: 0;
  }
}

.score-group {
  margin-left: 15px;
}

.score-group .el-radio-button__inner {
  padding: 8px 20px;
  font-size: 16px;
}
</style>
