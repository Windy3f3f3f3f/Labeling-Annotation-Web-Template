import axios from "./index";

/**
 * The structure of the data returned by the backend that needs to be annotated
 */
export interface IAnnotationData {
  id: number;
  textA: string;
  textB: string;
}

/**
 * Annotation result
 */
export interface ISubmitAnnotation {
  dataId: number;
  userName: string;
  score: number;
}

/**
 * Get the next data that needs to be annotated
 */
export async function fetchNextAnnotationData(
  userName: string
): Promise<IAnnotationData | null> {
  const response = await axios.get(`/api/annotation/next`, {
    params: { username: userName },
  });
  return response.data;
}

/**
 * Submit the annotation result
 */
export async function submitAnnotation(
  annotation: ISubmitAnnotation
): Promise<void> {
  await axios.post("/api/annotation/submit", annotation);
}

/**
 * Get the annotation progress of the user
 */
export async function getAnnotationProgress(
  userName: string
): Promise<{ completed: number; total: number }> {
  try {
    const response = await axios.get(`/api/annotation/progress`, {
      params: { username: userName },
    });
    return response.data;
  } catch (error) {
    console.error("Error fetching progress:", error);
    throw error;
  }
}
